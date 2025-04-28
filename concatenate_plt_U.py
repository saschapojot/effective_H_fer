import re
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import warnings
from scipy.stats import ks_2samp
import sys
import os
import math
from pathlib import Path
from datetime import datetime
import glob
from decimal import Decimal, getcontext

#this script concatenates and plots U from pkl files
def format_using_decimal(value, precision=8):
    # Set the precision higher to ensure correct conversion
    getcontext().prec = precision + 2
    # Convert the float to a Decimal with exact precision
    decimal_value = Decimal(str(value))
    # Normalize to remove trailing zeros
    formatted_value = decimal_value.quantize(Decimal(1)) if decimal_value == decimal_value.to_integral() else decimal_value.normalize()
    return str(formatted_value)
N=60
Nx=N
Ny=N
Nz=N

init_path_num=0
T=1.3
eps_for_auto_corr=5e-1
# P=0.1
TStr=format_using_decimal(T)

# PStr=format_using_decimal(P)
total_atom_xyz_components_num=Nx*Ny*Nz*3*3
total_atom_num=Nx*Ny*Nz*3
total_molecule_num=Nx*Ny*Nz

#read all or some of the pkl files
n_dig=8

def sort_data_files_by_flushEnd(oneDir):
    dataFilesAll=[]
    flushEndAll=[]
    for oneDataFile in glob.glob(oneDir+"/flushEnd*.pkl"):
        dataFilesAll.append(oneDataFile)
        matchEnd=re.search(r"flushEnd(\d+)",oneDataFile)
        if matchEnd:
            indTmp=int(matchEnd.group(1))
            flushEndAll.append(indTmp)

    endInds=np.argsort(flushEndAll)
    sortedDataFiles=[dataFilesAll[i] for i in endInds]
    return sortedDataFiles
U_pkl_dir=f"./dataAll/N{N}/T{TStr}/init_path{init_path_num}/U_dipole_dataFiles/U/"

print(U_pkl_dir)
flushEnd_vals_all=[]
file_names_all=[]
for file in glob.glob(U_pkl_dir+"/flushEnd*.pkl"):
    match_num=re.search(r"flushEnd(\d+).U",file)
    if match_num:
        file_names_all.append(file)
        flushEnd_vals_all.append(int(match_num.group(1)))


sortedInds=np.argsort(flushEnd_vals_all)
# print(file_names_all)
sorted_flushEnd_vals_all=[flushEnd_vals_all[ind] for ind in sortedInds]

sorted_file_names_all=[file_names_all[ind] for ind in sortedInds]

startingFileInd=0
startingFileName=sorted_file_names_all[startingFileInd]
# print(sorted_file_names_all)
with open(startingFileName,"rb") as fptr:
    inArrStart=pickle.load(fptr)


U_arr=inArrStart
for pkl_file in sorted_file_names_all[(startingFileInd+1):]:
    with open(pkl_file,"rb") as fptr:
        inArr=pickle.load(fptr)
    U_arr=np.append(U_arr,inArr)

print(f"len(U_arr)={len(U_arr)}")
U_starting_ind=600
print(U_arr[-10:])
plt.figure()
plt.plot(range(U_starting_ind,len(U_arr)),U_arr[U_starting_ind:],color="black")
plt.title(f"U_init_{init_path_num}.png")
plt.savefig(f"U_init_{init_path_num}.png")
plt.close()
# def auto_corrForOneVec(vec):
#     """
#
#     :param colVec: a vector of data
#     :return:
#     """
#     same=False
#     NLags=int(len(vec)*3/4)
#     with warnings.catch_warnings():
#         warnings.filterwarnings("error")
#     try:
#         acfOfVec=sm.tsa.acf(vec,nlags=NLags)
#     except Warning as w:
#         same=True
#
#     acfOfVecAbs=np.abs(acfOfVec)
#     minAutc=np.min(acfOfVecAbs)
#     lagVal=-1
#     print(f"minAutc={minAutc}")
#     if minAutc<=eps_for_auto_corr:
#         lagVal=np.where(acfOfVecAbs<=eps_for_auto_corr)[0][0]
#
#     return same,lagVal
#
# arr_selected=U_arr[-60:]
#
# print(auto_corrForOneVec(arr_selected))