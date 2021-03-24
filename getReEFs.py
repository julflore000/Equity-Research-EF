import numpy as np
import pandas as pd 
from geopy.geocoders import Nominatim
from stateAbrevationsMap import us_state_abbrev
import math


def getDeclineFactors(plantDataset,year):
    """returns a list that contains the decline factor for each plant in that year

    Args:
        plantDataset (panda): plants considered
        year (int): year of study for EFs
    """
    if year <= 2020:
        #just return a list of decline factors that are zero (no decline) if year <= 2020
        return [[0,0]] * len(plantDataset)
    #read in decline factors into main dataset, contains capital expenditure declines (installation/construction) & operational expenditures (O&M)
    declineFactorDataset = pd.read_excel(("EF_data/declineFactors.xlsx"))
        
    #round to the nearest multiple of value below (in this case it is 5, so we have values for 2020, 2025, 2030....2050)
    roundOn = 5
    
    #getting lower decline factor- from this lower decline year we also know the upper decline year as each column is only in 5 year increments
    roundDownYear = roundOn * round(math.floor(year/roundOn))
    roundUpYear = roundDownYear + 5
    
    #*** since all plants are treated as getting the same decline factor we really only need to compute the decline factors for wind & solar once
     
    ############# SOLAR DECLINE FACTOR CALCULATION START #############
    
    #if solar plant we will be getting the bottom two rows which contain utility and residential solar- leading to an average
    
    #get out capital expenditures average of utility and res for solar bottom year
    capexBottomDeclineEF = (declineFactorDataset["CAPEX " +(str(roundDownYear))][1] + declineFactorDataset["CAPEX " +(str(roundDownYear))][2])/2
    
    #repeat for rounded up year
    capexTopDeclineEF = (declineFactorDataset["CAPEX " +(str(roundUpYear))][1] + declineFactorDataset["CAPEX " +(str(roundUpYear))][2])/2
    
    #gives us the annual change in decline factor from previous rounded year to next, uses linear interpolation
    annualCapexDecline = (capexTopDeclineEF-capexBottomDeclineEF)/roundOn

    #calculate final CAPEX decline factor, will be the lower bound + (years from bottom)*annualDecline
    solarCapexDeclineFactor = capexBottomDeclineEF + annualCapexDecline* (year-roundDownYear)
    
    #repeat the same process as above but with OPEX-operational expenditures
    opexBottomDeclineEF = (declineFactorDataset["OPEX " +(str(roundDownYear))][1] + declineFactorDataset["OPEX " +(str(roundDownYear))][2])/2
    
    opexTopDeclineEF = (declineFactorDataset["OPEX " +(str(roundUpYear))][1] + declineFactorDataset["OPEX " +(str(roundUpYear))][2])/2
    
    annualOpexDecline = (opexTopDeclineEF-opexBottomDeclineEF)/roundOn

    #calculate final OPEX decline factor, will be the lower bound + (years from bottom)*annualDecline
    solarOpexDeclineFactor = opexBottomDeclineEF + annualOpexDecline* (year-roundDownYear)
    
    ############# SOLAR DECLINE FACTOR CALCULATION END #############


    ############# WIND DECLINE FACTOR CALCULATION START #############
    
    #if wind plant we will be getting only the top row of data
    #get out capital expenditures 
    capexBottomDeclineEF = declineFactorDataset["CAPEX " +(str(roundDownYear))][0]
    
    #repeat for rounded up year
    capexTopDeclineEF = declineFactorDataset["CAPEX " +(str(roundUpYear))][0]
    
    #gives us the annual change in decline factor from previous rounded year to next, uses linear interpolation
    annualCapexDecline = (capexTopDeclineEF-capexBottomDeclineEF)/roundOn

    #calculate final CAPEX decline factor, will be the lower bound + (years from bottom)*annualDecline
    windCapexDeclineFactor = capexBottomDeclineEF + annualCapexDecline* (year-roundDownYear)

    #repeat same process as above for OPEX
    opexBottomDeclineEF = declineFactorDataset["OPEX " +(str(roundDownYear))][0]
    
    opexTopDeclineEF = declineFactorDataset["OPEX " +(str(roundUpYear))][0]
    
    annualOpexDecline = (opexTopDeclineEF-opexBottomDeclineEF)/roundOn
    
    windOpexDeclineFactor = opexBottomDeclineEF + annualOpexDecline* (year-roundDownYear)        
    
    ############# WIND DECLINE FACTOR CALCULATION END #############

    #create final list that mirrors the plant dataset but holds [CAPEX decline factor, OPEX decline factor
    declineFactorList = []
    #run through each of the plants technology
    for plantDetails in plantDataset:
        #should either be a "S" for solar or "W" for wind
        plantTech = plantDetails[2]
        
        if plantTech == "S": 
            #return the solar decline factors, first the capital then the operational
            declineFactorList.append([solarCapexDeclineFactor,solarOpexDeclineFactor])
        else:
            #return the wind decline factors, first the capital then the operational
            declineFactorList.append([windCapexDeclineFactor,windOpexDeclineFactor])  
        
    #once done we are left with a list of the respective decline factors
    return declineFactorList
 
 
            
def getReEFs(rePlantList,year):
    """returns the employment factor for each lat long in panda dataframe, need to specify wind or solar
    At state level dimension

    Args:
        rePlantList ([list]): [[lat,long, and either a "S" or "W" for wind or solar]]
    """ 
    # initialize Nominatim API  
    geolocator = Nominatim(user_agent="renewableEnergyEFs")
    
    #read in solar and wind EF data for each state
    renewableEFsDataset = pd.read_excel("EF_data/reEFs.xlsx")

    
    #getting the total decline factors for that year and for all plants
    declineFactorList = getDeclineFactors(rePlantList,year)
    #creation of final renewable EF dict, will convert to panda dataframe at end
    reEFDict = dict()
    
    #run through each of the lat longs and RE points
    for plantDetails,declineFactor in zip(rePlantList,declineFactorList):
        lat = plantDetails[0]
        long = plantDetails[1]
        #get out the full details of location
        location = geolocator.reverse(f"{lat},{long}")
        
        state = location.raw['address'].get('state', '')
        
        #state Abreviations
        stateAbrev = us_state_abbrev[state]
        
        plantRowLocation = np.where(renewableEFsDataset["State"] == stateAbrev)[0][0]
        #if asking for solar plant, returns construction and then O&M EFs, else if wind then return single EF
        if plantDetails[2] == "S":
            #multiply by (1-declineFactor) of either Capex-0 position or OPEX-1 position
            reEFDict[lat+","+long+","+plantDetails[2]] = [renewableEFsDataset["PV Con/Instl EF"][plantRowLocation]* (1-declineFactor[0]), renewableEFsDataset["PV O&M EF"][plantRowLocation]*(1-declineFactor[1])]
        else:
            #for wind right now I am taking the average of the two decline factors-WILL MOST LIKELY CHANGE
            reEFDict[lat+","+long+","+plantDetails[2]] = [renewableEFsDataset["WT Total EF"][plantRowLocation] * (1-(declineFactor[0] +declineFactor[1])/2)]

    #transforming renewable EF dict into panda dataframe 
    pandaReEF = pd.DataFrame.from_dict(reEFDict,orient='index',columns=['Con/Instl EF','O&M EF'])
    
    return pandaReEF