# Equity Research EFs
 Module for providing wind, solar, and coal job years/MW EFs based on location
 * Current functionality: Unable to find state level job resolution borken down into O&M and con/instl sectors so currently using static values

### Modules to Install
* Need to install geopy used to calculate which state that hypothetical plant is in
    
    if in anaconda terminal run: 
    conda install -c conda-forge geopy
### Data Sources:
* Solar state level capacities was taken from https://seia.org/states-map
* Solar Jobs data from https://www.solarstates.org/#states/solar-jobs/2019

* Wind job values come from: Job creation during the global energy transition towards 100% renewable power system by 2050 due to inability to find wind jobs at a state level with breakdown of O&M and construction/installation


* For  coal jobs , a static value of .14 jobs/MW is being used due to poor data source resolution- see source below

Job creation during the global energy transition towards 100% renewable power system by 2050 

* State Abbreviations dict used graciously taken from: https://gist.github.com/rogerallen/1583593


States and their abbreviations included in this module:
* All states except AK and HI
* **Make sure to check each state's EFs in the reEFs.xlsx file (may need to replace outliers with agreed upon values) before each simulation run**
### How to use:

`getCoalEFs`: Input list of coal plant codes- see EIA dataset 6_2_EnviroEquip_Y2019.xlsx from EIA 860 for details, will then return 
panda data frame with each row being the plant name and then the EF in its respective row.

Example: 
    
    testPlantList = ["1573","1588","2517"] #unique plants in MD, MA, and NY respectively

    #returns in panda dataframe set up
    coalEFs = getCoalEFs(testPlantList)

Old version of returned dataset using EIA capacities (will now return a single static value: .14)


                        Plant EF
    Bridgeport Station  0.132500
    Merrimack           0.209227
    Brandon Shores      0.457080

* Current Implementation: due to inadequate job statistics on a state level basis, a single EF is used for employment factors. This value is from the paper: Job creation during the global energy transition towards 100% renewable power system by 2050 (.14 jobs/MW for O&M). Returns single value

`getCoalDecom`: returns the static value of job-years/MW created for decommissioning a coal plant, data comes from the paper:  Job creation during the global energy transition towards 100% renewable power system by 2050 
    
`getReEFs`: Input list of lat and long of plant as well as whether its solar or not, include in list within list. Also input year of analysis after list in module call

**WARNING:** Solar EFs may not be accurate due to data source used. Check the reEFs xlsx for more info on a state by state basis to see the details. Possible solution to outliers is to replace with a common research value (more research is needed on this topic), can use the job creation during the global energy transition paper for substitute values.


Example: 

    #gets first solar then wind EFs for that location (at state level which in this case is Boston)
    testPlantList = [["42.360081","-71.058884", "S"],["42.360081","-71.058884", "W"]] 


    #can put in string of either 'res' 'util' or 'avg'(averages the two) to get the respective decline factors for that solar tech
    optionalDeclineFactor = "avg"

    #returns in panda data frame set up
    renewableEFs = getReEFs(testPlantList,2020,optionalDeclineFactor)

    #final format will be in two manners
    if solar selected
        key "lat,long,S" = [Construction PV EF * (1-CAPEX decline), O&M PV EF * (1-OPEX decline)]
    if wind selected
        key "lat,long,W" = [Construction WT EF * (1-CAPEX decline), O&M WT EF * (1-OPEX decline)]

* CAPEX: capital expenditures (installation & construction)
* OPEX: operational expenditures (operations & maintenance)


Example returned dataset for same coordinate with different keys(<=2020 there is no decline factor).


                            Con/Instl EF    O&M EF
    42.360081,-71.058884,S      1.056212  0.320726
    42.360081,-71.058884,W      0.240000  0.300000


* Note: for converting the solar construction jobs/MW to job-years/MW we divided the jobs by the expected lifetime of the plant: 30 years taken from  Job creation during the global energy transition towards 100% renewable power system by 2050

* Note 2: O&M EF was taken from same source above, con/instl EF was taken from same source multiplied by projection lifetime (2 years) then divided by average lifetime: 2 (con/instl period) * 3 (con/instl EF) /25 (WT onshore wind lifetime)= .24 job-years/MW