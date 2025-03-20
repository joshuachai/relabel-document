#!/usr/bin/env python3
import os
import sys
import glob
import pandas as pd
from pathlib import Path

def decomposeFileName(studyID, inst, layer, mm, scans, filename):
    
    tag = ""
    
    studyID = filename.split("_")[0]
    tag = filename.split("_")[1]
    tag = tag.split(".")[0]
    if tag[0] == "S":
        inst = "Spectralis"
        mm = tag[-1]
        mm += "x"
        mm += tag[-1]
        scans = "512x512"
    elif tag[0] == "R":
        inst = "Revo"
        
    if not "H" in tag:
        if tag[1:-1] == "R":
            layer = "Retina"
        elif tag[1:-1] == "S":
            layer = "Superficial"
        elif tag[1:-1] == "SVC":
            layer = "SVC"
        elif tag[1:-1] == "SVP":
            layer = "SVP"
        elif tag[1:-1] == "DVC":
            layer = "DVC"
        elif tag[1:-1] == "DCP":
            layer = "DCP"
        elif tag[1:-1] == "D":
            layer = "Deep"
    else:
        if tag[1:-2] == "R":
            layer = "Retina"
        elif tag[1:-2] == "S":
            layer = "Superficial"
        elif tag[1:-2] == "SVC":
            layer = "SVC"
        elif tag[1:-2] == "SVP":
            layer = "SVP"
        elif tag[1:-2] == "DVC":
            layer = "DVC"
        elif tag[1:-2] == "DCP":
            layer = "DCP"
        elif tag[1:-2] == "D":
            layer = "Deep"
        
    return studyID, inst, layer, mm, scans

def ExtractFileInfo(instrument, size, tag):
    
    fileInfo = ""
    
    if instrument == "revo":
        fileInfo += "R"
    elif instrument == "spectralis":
        fileInfo += "S"
    
    if "Retina" in tag:
        fileInfo += "R"
    elif "Superficial" in tag:
        fileInfo += "S"
    elif "SVC" in tag:
        fileInfo += "SVC"
    elif "SVP" in tag:
        fileInfo += "SVP"
    elif "DVC" in tag:
        fileInfo += "DVC"
    elif "DCP" in tag:
        fileInfo += "DCP"
    elif "Deep" in tag:
        fileInfo += "D"
        
    if size == 3.3 or size == 3.5 or size == 3.6:
        fileInfo += "3"
    elif size == 3.4:
        fileInfo += "3H"
    elif size == 6.4:
        fileInfo += "6"
    elif size == 10.6:
        fileInfo += "10"
    
    return fileInfo

def revo(imageID_list):
    print("revo")
    filename = ""
    fileInfo = ""
    fileExtension = ""
    studyID = ""
    instrument = "Revo"
    retinalLayer = ""
    imageSizeMM = ""
    imageSizeScans = ""
    
    for dirpath, dirs, files in os.walk("./REVO", topdown=False):
        if files and not dirs:
            for filename in files:
                if filename and not filename.startswith(".") and "." in filename and " " in filename:            
                    fileExtension = filename.split(".")[-1]
                    size = dirpath.split("/")[-1]
                    size = int(float(size.replace("_", ".")) * 10) / 10
                    fileInfo = ExtractFileInfo("revo", size, filename.split("_")[1])
                    #print(filename + dirpath)
                    target = os.path.join(dirpath, filename)
                    studyID = dirpath.split("/")[-2]
                    studyID = studyID[:4] + "-" + studyID[4:]
                    newFilename = studyID + "_" + fileInfo + "." + fileExtension
                    newName = os.path.join(dirpath, newFilename)
                    os.rename(target, newName)
                    #print(filename + " has been changed to " + newFilename)
                else:
                    continue
                
    for dirpath, dirs, files in os.walk("./REVO", topdown=False):
        if files and not dirs:
            for filename in files:
                if filename and not filename.startswith(".") and "." in filename:
                    fileExtension = filename.split(".")[-1]
                    size = dirpath.split("/")[-1]
                    imageSizeMM = size.split("_")[0] + "x" + size.split("_")[0]
                    imageSizeScans = size.split("_")[1] + "x" + size.split("_")[1]
                    studyID, instrument, retinalLayer, imageSizeMM, imageSizeScans = decomposeFileName(studyID, instrument, retinalLayer, imageSizeMM, imageSizeScans, filename)                    
                    for imageID, OCTA, inst, layer, mm, scans in imageID_list:
                        if OCTA == studyID and inst == instrument and layer == retinalLayer and mm == imageSizeMM and imageSizeScans == scans:
                            # Set an original file name
                            target = os.path.join(dirpath, filename)
                            # Set a new name
                            if int(imageID) < 1000:
                                final = os.path.join(dirpath, "0" + str(imageID) + "." + fileExtension)
                            else:
                                final = os.path.join(dirpath, str(imageID) + "." + fileExtension)
                            # Rename
                            os.rename(target, final)
                            # Result message
                            if int(imageID) < 1000:
                                print(filename + " has been changed to " + "0" + str(imageID) + "." + fileExtension)
                            else:
                                print(filename + " has been changed to " + str(imageID) + "." + fileExtension)
                        else:
                            continue
                    
            
# Relable the file name generated by Spectralis
def spectralis(name_list, imageID_list):
    print("spectralis")
    filename = ""
    fileInfo = ""
    fileExtension = ""
    studyID = ""
    instrument = "Spectralis"
    retinalLayer = ""
    imageSizeMM = "3x3"
    imageSizeScans = "512x512"
    
    # Set a path
    path = Path("./Spectralis")
    for filenames in path.iterdir():
        # Since path.iterdir() returns entire path of file, it should be extracted
        filename = filenames.parts[-1]
        # Set a filter to remove unnecessary files (such as .dsstore or any other confiuration file/dummy)
        if filename and not filename.startswith(".") and "." in filename and " " in filename:
            # Extract the file extension
            fileExtension = filename.split(".")[-1]
            # Extract the size of photo, instrument name, and retinal layer
            fileInfo = ExtractFileInfo("spectralis", 3.3, filename.split(" ")[-3])
            # Combine each other's data to rename it
            filename = filename.split(" ")[0] + " " + filename.split(" ")[1]            
        else:
            # Disregard it if it is not appropriate file
            continue
        for givenname, surname, studyID in name_list:
            if filename.strip() == (str(surname) + " " + str(givenname)).strip():
                #print(studyID + "_" + fileInfo + "." + fileExtension)
                # Set an original file name
                target = os.path.join("./Spectralis", filenames.parts[-1])
                # Set a new name
                newName = os.path.join("./Spectralis", studyID + "_" + fileInfo + "." + fileExtension)
                # Rename
                os.rename(target, newName)
                # Result message
                print(filenames.parts[-1] + " has been changed to " + studyID + "_" + fileInfo + "." + fileExtension)
                
    for filenames in path.iterdir():
        # Since path.iterdir() returns entire path of file, it should be extracted
        filename = filenames.parts[-1]
        # Set a filter to remove unnecessary files (such as .dsstore or any other confiuration file/dummy)
        if filename and not filename.startswith(".") and "." in filename:
            studyID, instrument, retinalLayer, imageSizeMM, imageSizeScans = decomposeFileName(studyID, instrument, retinalLayer, imageSizeMM, imageSizeScans, filename)
            # Extract the file extension
            fileExtension = filename.split(".")[-1]
        else:
            # Disregard it if it is not appropriate file
            continue
        for imageID, OCTA, inst, layer, mm, scans in imageID_list:
            if OCTA == studyID and inst == instrument and layer == retinalLayer and mm == imageSizeMM and imageSizeScans == scans:
                # Set an original file name
                target = os.path.join("./Spectralis", filename)
                # Set a new name
                final = os.path.join("./Spectralis", str(imageID) + "." + fileExtension)
                # Rename
                os.rename(target, final)
                # Result message
                print(filename + " has been changed to " + str(imageID) + "." + fileExtension)
                

# Starting function
def extractFileName():
    
    # If user put appropriate number of argument, it will move on next step
    if len(sys.argv) == 2:
        # arg1 store the parametre which instrument user does want to relable
        arg1 = sys.argv[1]  
        print(f"First argument: {arg1}")
    else:
        # If user put inappropriate number of argument, it will notify the usage and exit the programme
        print("Usage : ./relable.py {instrument name}")
        exit()
    
    # Open the excel file to compare file names
    df = pd.read_excel('2024_PartialData.xlsx')
    df2 = pd.read_excel('2025_OCTA_HARMONISATION_LABELS.xlsx')
    
    name_list = []
    imageID_list = []
    
    # Extract each rows
    # col2 : Givenname
    # col3 : Surname
    # col4 : Study ID
    for index, row in df.iterrows():
        col2 = row.iloc[0]  
        col3 = row.iloc[1]
        col4 = row.iloc[2]
        name_list.append([col2, col3, col4])
    
    for index, row in df2.iterrows():
        col2 = row['Image ID']  
        col3 = row['Study participant ID']
        col4 = row['Instrument']
        col5 = row['Retinal Layer']
        col6 = row['Image size [mm]']
        col7 = row['Image size [scans]']
        imageID_list.append([col2, col3, col4, col5, col6, col7]) 
    
    if (sys.argv[1] == "revo"):
        # If the argument is revo, it will excute the function named 'revo'
        revo(imageID_list)
    elif (sys.argv[1] == "spectralis"):
        # If the argument is 'spectralis', it will excute the function named 'spectralis'
        spectralis(name_list, imageID_list)
        

extractFileName()