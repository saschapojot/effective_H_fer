import numpy as np
import glob
import sys
import re
import matplotlib.pyplot as plt
from datetime import datetime
import json
import pandas as pd
import scipy.stats as stats
import pickle
import statsmodels.api as sm
import warnings
#this script computes auto-correlation for U data
# for all T
#this file deals with data in the original pkl files
if (len(sys.argv)!=3):
    print("wrong number of arguments")
    exit()

N=int(sys.argv[1])
init_path=int(sys.argv[2])
pkl_data_root=f"../dataAll/N{N}/"
csv_data_root=pkl_data_root+f"/csvOut_init_path{init_path}/"
TVals=[]
TFileNames=[]

for TFile in glob.glob(pkl_data_root+"/T*"):

    matchT=re.search(r"T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)",TFile)
    # if float(matchT.group(1))<1:
    #     continue

    if matchT:
        TFileNames.append(TFile)
        TVals.append(float(matchT.group(1)))


sortedInds=np.argsort(TVals)
sortedTVals=[TVals[ind] for ind in sortedInds]
sortedTFiles=[TFileNames[ind] for ind in sortedInds]
def sort_data_files_by_flushEnd(pkl_dir):
    dataFilesAll=[]
    flushEndAll=[]
    for oneDataFile in glob.glob(pkl_dir+"/flushEnd*.pkl"):
        dataFilesAll.append(oneDataFile)
        matchEnd=re.search(r"flushEnd(\d+)",oneDataFile)
        if matchEnd:
            flushEndAll.append(int(matchEnd.group(1)))
    endInds=np.argsort(flushEndAll)
    sortedDataFiles=[dataFilesAll[i] for i in endInds]

    return sortedDataFiles
def concatenate_U_pkl_files(sorted_U_DataFilesToRead,startingFileInd):
    U_StaringFileName=sorted_U_DataFilesToRead[startingFileInd]
    with open(U_StaringFileName,"rb") as fptr:
        U_inArrStart=np.array(pickle.load(fptr))
    UVec=U_inArrStart
    for pkl_file in sorted_U_DataFilesToRead[(startingFileInd+1):]:
        with open(pkl_file,"rb") as fptr:
            in_UArr=pickle.load(fptr)
            UVec=np.append(UVec,in_UArr)
    return UVec
def auto_corrForOneVec(vec):
    """

    :param colVec: a vector of data
    :return: acfOfVecAbs
    """
    same=False
    NLags=int(len(vec))
    with warnings.catch_warnings():
        warnings.filterwarnings("error")
    try:
        acfOfVec=sm.tsa.acf(vec,nlags=NLags)
    except Warning as w:
        same=True
    acfOfVecAbs=np.abs(acfOfVec)
    #the auto-correlation values correspond t0 lengths 0,1,...,NLags-1
    return acfOfVecAbs
def auto_corr_U_one_T(oneTStr,init_path,startingFileInd,varName):
    pkl_dir=oneTStr+f"/init_path{init_path}/U_dipole_dataFiles/{varName}/"

    sorted_U_DataFilesToRead=sort_data_files_by_flushEnd(pkl_dir)

    # print(sorted_U_DataFilesToRead)
    UVec=concatenate_U_pkl_files(sorted_U_DataFilesToRead,startingFileInd)
    acfOfVecAbs=auto_corrForOneVec(UVec)
    matchT=re.search(r'T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)',oneTFile)

    TStr=matchT.group(1)
    csv_out_dir=csv_data_root+f"/T{TStr}/"
    out_corr_file_name=csv_out_dir+"/U_corr.csv"
    df=pd.DataFrame(acfOfVecAbs)
    df.to_csv(out_corr_file_name,header=False, index=False)

tStart=datetime.now()
varName="U"
startingfileIndTmp=5
sweep_multiple=70
lagTmp=10
for k in range(0,len(sortedTFiles)):
    oneTFile=sortedTFiles[k]
    auto_corr_U_one_T(oneTFile,init_path,startingfileIndTmp,varName)

tEnd=datetime.now()

print(f"time: {tEnd-tStart}")


