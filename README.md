# Equity Research EFs
 Module for providing wind, solar, and coal EFs based on location
 * Key point: single EF supplied for Wind while two EFs supplied for O&M and installation/construction (estimated 25 year life span of solar plants)
### Modules to Install
* Need to install geopy used to calculate which state that hypothetical plant is in
    
    if in anaconda run: 
    conda install -c conda-forge geopy
### Data Sources:
* Solar state level capacities was taken from https://seia.org/states-map
* Solar Jobs data from https://www.solarstates.org/#states/solar-jobs/2019

* Wind capacity from EIA dataset: https://www.eia.gov/electricity/data/eia860/
* Wind jobs rounded in three bins used in paper Employment factors for wind and solar energy technologies: A literature review https://www.sciencedirect.com/science/article/abs/pii/S1364032115000118

* Coal capacity for each state also from EIA dataset: EIA 860
* Coal electric generation jobs from BW Research state level reports: https://static1.squarespace.com/static/5a98cf80ec4eb7c5cd928c61/t/5c7f375515fcc0964aa19491/1551841115357/USEER+Energy+Employment+by+State.pdf

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

`getCoalEFs`: Input list of coal plant names-will check that the plant is conventional steam coal may need to change later will then return 
panda data frame with each row being the plant name and then the EF in its respective row

Example: 
    
    testPlantList = ["Bridgeport Station","Merrimack","Brandon Shores"]

    #returns in panda dataframe set up
    coalEFs = getCoalEFs(testPlantList)

Returned dataset for example


                        Plant EF
    Bridgeport Station  0.132500
    Merrimack           0.209227
    Brandon Shores      0.457080

    
`getReEFs`: Input list of lat and long of plant as well as whether its solar or not, include in list within list

Example: 
    
    testPlantList = [["42.360081","-71.058884", "S"],["42.360081","-71.058884", "W"]] - gets first solar then wind EFs for that location (at state level which in this case is Boston)
    
    #returns in panda dataframe set up
    renewableEFs = getReEFs(testPlantList)

    #final format will be in two manners
    if solar selected
        key "lat,long,S" = [Construction EF, O&M EF]
    if wind selected
        key "lat,long,W" = [single EF]

Example returned dataset for same coordinate with different keys, note that there was no second EF returned for wind, only a single value encapsulating both


                            Con/Instl EF    O&M EF
    42.360081,-71.058884,S      1.267455  0.320726
    42.360081,-71.058884,W      2.800000       NaN