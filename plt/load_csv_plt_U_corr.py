import numpy as np
import glob
import sys
import re
import matplotlib.pyplot as plt
from datetime import datetime
import json
import pandas as pd
import scipy.stats as stats
from pathlib import Path


#this script loads auto-correlation of U data for each T
# and plots auto-correlation of U for all T

if (len(sys.argv)!=3):
    print("wrong number of arguments")
    exit()

N=int(sys.argv[1])
init_path=int(sys.argv[2])

csvDataFolderRoot=f"../dataAll/N{N}/csvOut_init_path{init_path}/"
TVals=[]
TFileNames=[]

for TFile in glob.glob(csvDataFolderRoot+"/T*"):

    matchT=re.search(r"T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)",TFile)
    # if float(matchT.group(1))<1:
    #     continue

    if matchT:
        TFileNames.append(TFile)
        TVals.append(float(matchT.group(1)))


sortedInds=np.argsort(TVals)
sortedTVals=[TVals[ind] for ind in sortedInds]
sortedTFiles=[TFileNames[ind] for ind in sortedInds]

auto_corr_U_dir=csvDataFolderRoot+"/corr_U/"
Path(auto_corr_U_dir).mkdir(exist_ok=True,parents=True)

def plt_corr_U_one_T(oneTFile):
    matchT=re.search(r'T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)',oneTFile)
    TStr=matchT.group(1)

    corr_U_csv_file_name=oneTFile+"/U_corr.csv"
    corr_U_arr=np.array(pd.read_csv(corr_U_csv_file_name,header=None))

    plt.figure()
    plt.plot(range(0,len(corr_U_arr)),corr_U_arr,color="black")
    plt.xlabel("separation")
    plt.ylabel("abs auto-correlation")
    plt.title(f"Abs auto-correlation, T={TStr}")
    plt.savefig(auto_corr_U_dir+f"/corr_U_T{TStr}.png")


tStart=datetime.now()
for k in range(0,len(sortedTFiles)):
    oneTFile=sortedTFiles[k]
    plt_corr_U_one_T(oneTFile)


tEnd=datetime.now()
print(f"time: {tEnd-tStart}")