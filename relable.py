#!/usr/bin/env python3
import os
import sys
import pandas as pd
from pathlib import Path

def ExtractFileInfo(instrument, size, tag):
    
    fileInfo = ""
    
    if instrument == "revo":
        fileInfo += "R"
    elif instrument == "spectralis":
        fileInfo += "S"
    
    if "Retina" in tag:
        fileInfo += "R"
    elif "SVC" in tag:
        fileInfo += "SVC"
    elif "SVP" in tag:
        fileInfo += "SVP"
    elif "DVC" in tag:
        fileInfo += "DVC"
    elif "DCP" in tag:
        fileInfo += "DCP"
        
    if size == 3.3:
        fileInfo += "3"
    elif size == 3.4:
        fileInfo += "3H"
    elif size == 6.4:
        fileInfo += 6.4
    
    return fileInfo

def revo():
    print("revo")
    filename = ""
    fileInfo = ""
    fileExtension = ""
    
    for dirpath, dirs, files in os.walk("./REVO", topdown=False):
        if files and not dirs:
            for filename in files:
                if filename and not filename.startswith(".") and "." in filename and " " in filename:            
                    fileExtension = filename.split(".")[-1]
                    fileInfo = ExtractFileInfo("revo", 3.3, filename.split(" ")[-3])
                    filename = filename.split(" ")[0] + " " + filename.split(" ")[1]            
                else:
                    continue


def spectralis(name_list, imageID_list):
    print("spectralis")
    filename = ""
    fileInfo = ""
    fileExtension = ""
    
    path = Path("./Spectralis")
    for filenames in path.iterdir():
        filename = filenames.parts[-1]
        if filename and not filename.startswith(".") and "." in filename and " " in filename:            
            fileExtension = filename.split(".")[-1]
            fileInfo = ExtractFileInfo("spectralis", 3.3, filename.split(" ")[-3])
            filename = filename.split(" ")[0] + " " + filename.split(" ")[1]            
        else:
            continue
        for givenname, surname, studyID in name_list:
            if filename.strip() == (str(surname) + " " + str(givenname)).strip():
                #print(studyID + "_" + fileInfo + "." + fileExtension)
                target = os.path.join("./Spectralis", filenames.parts[-1])
                newName = os.path.join("./Spectralis", studyID + "_" + fileInfo + "." + fileExtension)
                os.rename(target, newName)
                print(filenames.parts[-1] + " has been changed to " + studyID + "_" + fileInfo + "." + fileExtension)
                

def extractFileName():
    
    if len(sys.argv) == 2:
        arg1 = sys.argv[1]  
        print(f"First argument: {arg1}")
    else:
        print("Usage : ./relable.py {instrument name}")
        exit()
        
    df = pd.read_excel('2024_PartialData.xlsx')
    df2 = pd.read_excel('2025_OCTA_HARMONISATION_LABELS.xlsx')
    
    name_list = []
    imageID_list = []
    
    for index, row in df.iterrows():
        col2 = row.iloc[0]  
        col3 = row.iloc[1]
        col4 = row.iloc[2]
        name_list.append([col2, col3, col4])
    
    for index, row in df2.iterrows():
        col2 = row.iloc[0]  
        col3 = row.iloc[1]
        imageID_list.append([col2, col3]) 
    
    if (sys.argv[1] == "revo"):
        revo()
    elif (sys.argv[1] == "spectralis"):
        spectralis(name_list, imageID_list)
        

extractFileName()