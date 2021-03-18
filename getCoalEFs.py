import numpy as np
import pandas as pd 
import os, sys


def getCoalEFs(coalPlantList):
    """returns the employment factor for each coal plant in panda dataframe
    At state level demension

    Args:
        coalPlantList ([list]): [includes the coal plants slated for retirement- should be from EIA 860]
    """  
    #read in coal plant data EF_data\coalEFs.xlsx
    coalPlantLocs = pd.read_excel("EF_data/coalPlantLocs.xlsx")
    
    #reads in state level coal EF
    stateEFs = pd.read_excel("EF_data/coalEFs.xlsx")
    
    #creation of  coal state dict, will change into EFs after loop
    coalEFDataframe = dict()
    
    #run through tech list to make sure plant is coal and then find state plant is in
    for plantName in coalPlantList:
        
        #finds which row that coal plant is in the excel EIA dataset
        plantRowLocation = np.where(coalPlantLocs["Plant Name"] == plantName)[0]
        
        #if multiple generators are called select the first row
        if len(plantRowLocation) > 1:
            plantRowLocation = plantRowLocation[0]
        
        #getting the technology of that plant
        plantTech = coalPlantLocs["Technology"][plantRowLocation]
        
        #checking to make sure that the plant is labeled as Conventional Steam Coal, needs to be the only technology
        if (plantTech != "Conventional Steam Coal"):
            raise ValueError(f"The plant {plantName} is not labeled as conventional steam coal, its labeled as {plantTech}!")
            print(f"Skipping {plantName} for now however errors may develop later on. :O")
            continue
        else:
            #gets state and assigns into a dict with key as plant name
            coalEFDataframe[plantName] = coalPlantLocs["State"][plantRowLocation]
    
    #final coal dict set up
    coalEFPandaDf = dict()
    #run through the EF list assigning EF values for each state
    for plantName in coalEFDataframe.keys():
        
        #finds which row that state is in the EF dataset
        plantRowLocation = np.where(stateEFs["State"] == coalEFDataframe[plantName])[0][0]

        #updating coalEFDataFrame to for it to carry the respective EF of that state
        coalEFPandaDf[plantName] = stateEFs["Coal EFs"][plantRowLocation]
    
    #transforming coal EF dict into panda dataframe 
    pandaCoalEF = pd.DataFrame.from_dict(coalEFPandaDf,orient='index',columns=['Plant EF'])
    
    return pandaCoalEF