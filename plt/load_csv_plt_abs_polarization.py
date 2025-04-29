import numpy as np
import glob
import sys
import re
import matplotlib.pyplot as plt
from datetime import datetime
import json
import pandas as pd
import scipy.stats as stats
#This script loads avg dipole data, with confidence interval
# and plots magnitude of polarization for all T

if (len(sys.argv)!=3):
    print("wrong number of arguments")
    exit()

N=int(sys.argv[1])
init_path=int(sys.argv[2])

csvDataFolderRoot=f"../dataAll/N{N}/csvOut_init_path{init_path}/"

inCsvFile=csvDataFolderRoot+"/polarization_plot.csv"

df=pd.read_csv(inCsvFile)

TVec=np.array(df["T"])
PValsAll=np.array(df["P"])

mask = (TVec > 0.2)
TInds = np.where(mask)[0]
TInds=TInds[::1]
print(f"TInds={TInds}")
TToPlt=TVec[TInds]
print(TToPlt)

#plt P
fig,ax=plt.subplots()

ax.errorbar(TToPlt,PValsAll[TInds],fmt='o',color="black",
            ecolor='r', capsize=0.1,label='mc',
            markersize=1)

ax.set_xlabel('$T$')
ax.set_ylabel("$|P|$")
ax.set_title("norm of polarization, unit cell number="+str(N**2))
plt.legend(loc="best")
plt.savefig(csvDataFolderRoot+"/P_abs.png")
plt.close()