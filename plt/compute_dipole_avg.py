import numpy as np
import glob
import sys
import re
import matplotlib.pyplot as plt
from datetime import datetime
import json
import pandas as pd
import scipy.stats as stats

#this script converts Px, Py csv files to average for all T

if (len(sys.argv)!=3):
    print("wrong number of arguments")
    exit()

N=int(sys.argv[1])
init_path=int(sys.argv[2])
csvDataFolderRoot=f"../dataAll/N{N}/csvOut_init_path{init_path}/"
TVals=[]
TFileNames=[]

unitCellNum=N**2

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
polarization_abs_all=[]
def polarization_one_T(oneTFile):
    """

    :param oneTFile: corresponds to one temperature
    :return:
    """
    matchT=re.search(r'T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)',oneTFile)
    TVal=float(matchT.group(1))
    Px_path=oneTFile+"/Px.csv"
    Py_path=oneTFile+"/Py.csv"

    df_Px=np.array(pd.read_csv(Px_path,header=None))
    df_Py=np.array(pd.read_csv(Py_path,header=None))

    Px_avg=np.mean(df_Px,axis=0)
    Py_avg=np.mean(df_Py,axis=0)
    out_dipole_file_name=oneTFile+"/avg_dipole_combined.csv"
    out_arr=np.array([
        Px_avg,Py_avg
    ])
    df=pd.DataFrame(out_arr)
    df.to_csv(out_dipole_file_name, header=False, index=False)
    polarization_x=np.mean(Px_avg)
    polarization_y=np.mean(Py_avg)
    # print(f"polarization_x={polarization_x}, polarization_y={polarization_y}")
    P_abs=np.sqrt(polarization_x**2+polarization_y**2)
    return P_abs

tStart=datetime.now()

for k in range(0,len(sortedTFiles)):
    oneTFile=sortedTFiles[k]
    P_abs=polarization_one_T(oneTFile)
    polarization_abs_all.append(P_abs)


#write polarization_abs_all

csv_file_name=csvDataFolderRoot+"polarization_plot.csv"

df=pd.DataFrame({
    "T":sortedTVals,
    "P":polarization_abs_all
})


df.to_csv(csv_file_name,index=False)

tEnd=datetime.now()

print(f"time: {tEnd-tStart}")