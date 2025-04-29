import numpy as np
from datetime import datetime
import sys
import re
import glob
import os
import json
from pathlib import Path
import pandas as pd
import pickle

#this script extracts effective data from pkl files
# for U


if (len(sys.argv)!=4):
    print("wrong number of arguments")
    exit()


N=int(sys.argv[1])
TStr=sys.argv[2]
init_path=sys.argv[3]
summary_obs_name="U"
dataRoot=f"./dataAll/N{N}/T{TStr}/init_path{init_path}/"
csv_out_path=f"./dataAll/N{N}/T{TStr}/"


def parseSummary(summary_obs_name):
    startingFileInd=-1

    lag=-1
    sweep_to_write=-1
    smrFile=dataRoot+"/summary_"+summary_obs_name+".txt"

    summaryFileExists=os.path.isfile(smrFile)
    if summaryFileExists==False:
        return startingFileInd,-1

    with open(smrFile,"r") as fptr:
        lines=fptr.readlines()

    for oneLine in lines:
        #match startingFileInd
        matchStartingFileInd=re.search(r"startingFileInd=(\d+)",oneLine)

        if matchStartingFileInd:
            startingFileInd=int(matchStartingFileInd.group(1))
        # startingFileInd=35
        #match lag
        matchLag=re.search(r"lag=(\d+)",oneLine)
        if matchLag:
            lag=int(matchLag.group(1))

        #match sweep_to_write
        match_sweep_to_write=re.search(r"sweep_to_write=(\d+)",oneLine)

        if match_sweep_to_write:
            sweep_to_write=int(match_sweep_to_write.group(1))

    return startingFileInd,lag,sweep_to_write


def sort_data_files_by_flushEnd(summary_obs_name,varName):
    dataFolderName=dataRoot+"/U_dipole_dataFiles/"+varName+"/"

    dataFilesAll=[]
    flushEndAll=[]
    for oneDataFile in glob.glob(dataFolderName+"/flushEnd*.pkl"):
        dataFilesAll.append(oneDataFile)
        matchEnd=re.search(r"flushEnd(\d+)",oneDataFile)
        if matchEnd:
            flushEndAll.append(int(matchEnd.group(1)))

    endInds=np.argsort(flushEndAll)
    sortedDataFiles=[dataFilesAll[i] for i in endInds]

    return sortedDataFiles


def U_extract_ForOneT(startingFileInd,lag,varName):
    TRoot=dataRoot

    sorted_U_DataFilesToRead=sort_data_files_by_flushEnd(summary_obs_name,varName)

    U_StaringFileName=sorted_U_DataFilesToRead[startingFileInd]

    with open(U_StaringFileName,"rb") as fptr:
        U_inArrStart=np.array(pickle.load(fptr))

    UVec=U_inArrStart
    for pkl_file in sorted_U_DataFilesToRead[(startingFileInd+1):]:
        with open(pkl_file,"rb") as fptr:
            in_UArr=pickle.load(fptr)
            UVec=np.append(UVec,in_UArr)

    UVecSelected=UVec[::lag]

    return UVecSelected


def save_U_data(UVecSelected,oneTStr,varName,init_path):
    outCsvDataRoot=csv_out_path+"/csvOutAll/"
    outCsvFolder=outCsvDataRoot+f"/init_path{init_path}/"
    Path(outCsvFolder).mkdir(exist_ok=True,parents=True)
    outFileName=f"{varName}.csv"

    outCsvFile=outCsvFolder+outFileName

    df=pd.DataFrame(UVecSelected)
    # Save to CSV
    print(f"saving {outCsvFile}")
    df.to_csv(outCsvFile, index=False, header=False)


t_save_start=datetime.now()
startingfileIndTmp,lagTmp,sweep_to_writeTmp=parseSummary(summary_obs_name)

if startingfileIndTmp<0:
    print("summary file does not exist for "+TStr+" "+summary_obs_name)
    exit(0)

varName="U"
UVecSelected=U_extract_ForOneT(startingfileIndTmp,lagTmp,varName)

save_U_data(UVecSelected,TStr,varName, init_path)

t_save_End=datetime.now()
print(f"time: {t_save_End-t_save_start}")