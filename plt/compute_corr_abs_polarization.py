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


#this script computes auto-correlation for abs polarization
#for all T
# this file deals with data in the original pkl files

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

def concatenate_one_dipole_component_pkl_files(sorted_P_dataFilesToRead,startingFileInd,sweep_to_write):
    one_component_StartingFileName=sorted_P_dataFilesToRead[startingFileInd]


    with open(one_component_StartingFileName,"rb") as fptr:
        one_component_inArrStart=np.array(pickle.load(fptr))

    one_component_Arr=one_component_inArrStart.reshape((sweep_to_write,-1))

    #read the rest of  pkl files
    for pkl_file in sorted_P_dataFilesToRead[(startingFileInd+1):]:
        with open(pkl_file,"rb") as fptr:
            one_component_inArr=np.array(pickle.load(fptr))
        one_component_inArr=one_component_inArr.reshape((sweep_to_write,-1))
        one_component_Arr=np.concatenate((one_component_Arr,one_component_inArr),axis=0)


    return one_component_Arr

def P_to_mean(one_component_Arr):
    """

    :param one_component_Arr: array of all Px or Py
    :return: average over lattice of Px or Py
    """
    print(f"one_component_Arr.shape={one_component_Arr.shape}")
    P_one_component_all=np.mean(one_component_Arr,axis=1)
    return P_one_component_all


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

def auto_corr_abs_P_one_T(oneTStr,init_path,startingFileInd,sweep_to_write):
    varName_Px="Px"
    varName_Py="Py"

    pkl_Px_dir=oneTStr+f"/init_path{init_path}/U_dipole_dataFiles/{varName_Px}/"
    sorted_Px_pkl_files=sort_data_files_by_flushEnd(pkl_Px_dir)
    Px_Arr=concatenate_one_dipole_component_pkl_files(sorted_Px_pkl_files,startingFileInd,sweep_to_write)
    Px_mean_vec=P_to_mean(Px_Arr)

    pkl_Py_dir=oneTStr+f"/init_path{init_path}/U_dipole_dataFiles/{varName_Py}/"
    sorted_Py_pkl_files=sort_data_files_by_flushEnd(pkl_Py_dir)
    Py_Arr=concatenate_one_dipole_component_pkl_files(sorted_Py_pkl_files,startingFileInd,sweep_to_write)
    Py_mean_vec=P_to_mean(Py_Arr)

    abs_P_vec=np.sqrt(Px_mean_vec**2+Py_mean_vec**2)
    # print(oneTStr)
    # print(f"np.min(abs_P_vec)={np.min(abs_P_vec)}")
    # print(f"np.min(abs_P_vec)={np.min(abs_P_vec[-100:])}")
    acfOfVecAbs=auto_corrForOneVec(abs_P_vec)
    matchT=re.search(r'T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)',oneTFile)

    TStr=matchT.group(1)
    csv_out_dir=csv_data_root+f"/T{TStr}/"
    out_corr_file_name=csv_out_dir+"/abs_P_corr.csv"
    df=pd.DataFrame(acfOfVecAbs)
    df.to_csv(out_corr_file_name,header=False, index=False)



sweep_to_writeTmp=100
tStart=datetime.now()
startingfileIndTmp=5
for k in range(0,len(sortedTFiles)):
    oneTFile=sortedTFiles[k]
    auto_corr_abs_P_one_T(oneTFile,init_path,startingfileIndTmp,sweep_to_writeTmp)


tEnd=datetime.now()

print(f"time: {tEnd-tStart}")