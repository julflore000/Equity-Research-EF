# Equity Research EFs
 Module for providing wind, solar, and coal job years/MW EFs based on location
 * Key point: single EF supplied for Wind while two EFs supplied for O&M and installation/construction 

### Modules to Install
* Need to install geopy used to calculate which state that hypothetical plant is in
    
    if in anaconda terminal run: 
    conda install -c conda-forge geopy
### Data Sources:
* Solar state level capacities was taken from https://seia.org/states-map
* Solar Jobs data from https://www.solarstates.org/#states/solar-jobs/2019

* Wind capacity from EIA dataset: https://www.eia.gov/electricity/data/eia860/
* Wind jobs rounded in three bins used in paper Employment factors for wind and solar energy technologies: A literature review https://www.sciencedirect.com/science/article/abs/pii/S1364032115000118

* Coal capacity for each state also from EIA dataset: EIA 860 see wind dataset above
* Coal electric generation jobs from BW Research state level reports: https://static1.squarespace.com/static/5a98cf80ec4eb7c5cd928c61/t/5c7f375515fcc0964aa19491/1551841115357/USEER+Energy+Employment+by+State.pdf
* For the coal jobs above, a static value of .14 jobs/MW is being used due to poor data source resolution- see source below


* State Abbreviations dict used graciously taken from: https://gist.github.com/rogerallen/1583593


States and their abbreviations included in this module:
* CT: Connecticut
* DE: Delaware
* MA: Massachusetts
* MD: Maryland
* ME: Maine
* NH: New Hampshire
* NJ: New Jersey
* NY: New York
* OH: Ohio
* PA: Pennsylvania
* RI: Rhode Island
* VA: Virginia
* VT: Vermont
* WV: West Virginia

### How to use:

`getCoalEFs`: Input list of coal plant codes- see EIA dataset 6_2_EnviroEquip_Y2019.xlsx from EIA 860 for details, will then return 
panda data frame with each row being the plant name and then the EF in its respective row.

Example: 
    
    testPlantList = ["1573","1588","2517"] #unique plants in MD, MA, and NY respectively

    #returns in panda dataframe set up
    coalEFs = getCoalEFs(testPlantList)

Returned dataset for example


                        Plant EF
    Bridgeport Station  0.132500
    Merrimack           0.209227
    Brandon Shores      0.457080

* Current Implementation: due to inadequate job statistics on a state level basis, a single EF is used for employment factors. This value is from the paper: Job creation during the global energy transition towards 100% renewable power system by 2050 (.14 jobs/MW for O&M). Returns single value

`getCoalDecom`: returns the static value of job-years/MW created for decommissioning a coal plant (right now 1.65 job-years/MW), data comes from the paper:  Job creation during the global energy transition towards 100% renewable power system by 2050 
    
`getReEFs`: Input list of lat and long of plant as well as whether its solar or not, include in list within list. Also input year of analysis after list in module call

Example: 

    #gets first solar then wind EFs for that location (at state level which in this case is Boston)
    testPlantList = [["42.360081","-71.058884", "S"],["42.360081","-71.058884", "W"]] 


    #can put in string of either 'res' 'util' or 'avg'(averages the two) to get the respective decline factors for that solar tech
    optionalDeclineFactor = "avg"

    #returns in panda data frame set up
    renewableEFs = getReEFs(testPlantList,2020,optionalDeclineFactor)

    #final format will be in two manners
    if solar selected
        key "lat,long,S" = [Construction EF * (1-CAPEX decline), O&M EF * (1-OPEX decline)]
    if wind selected
        key "lat,long,W" = [single EF * (1-(CAPEX +OPEX)/2)]

* CAPEX: capital expenditures (installation & construction)
* OPEX: operational expenditures (operations & maintenance)


Example returned dataset for same coordinate with different keys, note that there was no second EF returned for wind, only a single value encapsulating both and since start year is less then time frame (<=2020 there is no decline factor).


                            Con/Instl EF    O&M EF
    42.360081,-71.058884,S      1.056212  0.320726
    42.360081,-71.058884,W      2.800000       NaN


* Note: for converting the solar construction jobs/MW to job-years/MW we divided the jobs by the expected lifetime of the plant: 30 years taken from  Job creation during the global energy transition towards 100% renewable power system by 2050

# Summary of work for at meeting (4/1)

# Coal EFs
    Due to the low level resolution in BW research jobs, the getCoalEFs() module simply returns a single value- won't even have to call that module but implementation is there for further down the line if we get higher resolution data (value using is .14 jobs/MW)
# RE Decline Factors
    can specify 'res'-residential decline factors for CAPEX and OPEX, 'util'-for utility decline factors, or "avg" (or leave input blank) for the average of the two decline factors
# Next Steps/Things to go over at meeting (3/25)

# 1 Wind Jobs
Wind jobs: it seems that the American Wind Energy Association or now American Clean Power is the place to go
for wind energy related statistics. Worth getting state level employment information at this point, or simply setting a static EFs for construction & O&M?

If interested this is the membership to get their info https://cleanpower.org/membership/

Cost: $500 dollars for academic membership (insane amounts once they start looking at other companies- pice tag in ranges of $100k +)

# 2 Decom EFs

- how important is it to have state level coal EFs, besides treating it as a single value from the global study paper


Coal decommissioning: implemented basic module for getCoalDecomEF(), single value from this paper: Job creation during the global energy transition towards 100% renewable power system by 2050, treated at 1.65 job-years/MW

From discussing with the authors that included these values, they based the claculations off a coal plant in Kosovo that retired and then spread that over to all the technologies, from the email they said that the results were "conservative"...- how does this get accepted?

# 3 Decline EFs

Employment factors changing with time as well: from the same research paper: Job creation during the global energy transition towards 100% renewable power system by 2050

Provide options for utility vs residential PV decline factors- believe we should be using utility however our overall solar EFs include residential jobs- question to bring up, right now averaging the two, see dataset in EF_data folder for more details

only applicable to REs, coal does not change

# can also work on changing lifetime as well for solar plants