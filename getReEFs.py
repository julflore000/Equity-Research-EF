import numpy as np
import pandas as pd 
from geopy.geocoders import Nominatim
from stateAbrevationsMap import us_state_abbrev

def getReEFs(rePlantList):
    """returns the employment factor for each lat long in panda dataframe, need to specify wind or solar
    At state level dimension

    Args:
        rePlantList ([list]): [[lat,long, and either a "S" or "W" for wind or solar]]
    """ 
    # initialize Nominatim API  
    geolocator = Nominatim(user_agent="renewableEnergyEFs")
    
    #read in solar and wind EF data for each state
    renewableEFsDataset = pd.read_excel("EF_data/reEFs.xlsx")

    
    #creation of final renewable EF dict, will convert to panda dataframe at end
    reEFDict = dict()
    
    #run through each of the lat longs and solar points
    for plantDetails in rePlantList:
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
            reEFDict[lat+","+long+","+plantDetails[2]] = [renewableEFsDataset["PV Con/Instl EF"][plantRowLocation], renewableEFsDataset["PV O&M EF"][plantRowLocation]]
        else:
            reEFDict[lat+","+long+","+plantDetails[2]] = [renewableEFsDataset["WT Total EF"][plantRowLocation]]

    #transforming renewable EF dict into panda dataframe 
    pandaREEF = pd.DataFrame.from_dict(reEFDict,orient='index',columns=['Con/Instl EF','O&M EF'])
    
    return pandaREEF