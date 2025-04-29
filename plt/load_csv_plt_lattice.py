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
from matplotlib.ticker import FormatStrFormatter  # Import formatter
#This script loads csv data of average dipole,
# and plots dipoles over lattice for all T
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

dipole_each_site_dir=csvDataFolderRoot+"/dipole_each_site/"
Path(dipole_each_site_dir).mkdir(exist_ok=True,parents=True)
def lattice_one_T(oneTFile):
    """

    :param oneTFile: corresponds to one temperature
    :return:
    """
    matchT=re.search(r'T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)',oneTFile)
    TStr=matchT.group(1)
    dipole_csv_file_name=oneTFile+"/avg_dipole_combined.csv"
    dipole_arr = np.array(pd.read_csv(dipole_csv_file_name, header=None))
    # The  rows: [Px, Py]
    Px = dipole_arr[0, :]
    Py = dipole_arr[1, :]
    # Compute the mean of the combined arrays
    avg_polarization_x = np.mean(Px)  # Mean of Px and Qx combined
    avg_polarization_y = np.mean(Py)  # Mean of Py and Qy combined
    # Print the results
    print(f"Average polarization along x (Px and Qx combined): {avg_polarization_x}")
    print(f"Average polarization along y (Py and Qy combined): {avg_polarization_y}")
    # Reshape the dipole components
    Px_arr = Px.reshape((N, N))
    Py_arr = Py.reshape((N, N))
    # Define the lattice constant
    a = 2
    # Instead of a flat list followed by meshgrid, generate index grids first.
    # Let n0 and n1 be the integer indices corresponding to the two lattice directions.
    n0 = np.arange(N)
    n1 = np.arange(N)
    # Use index ordering consistent with how the CSV was written
    # For a triangular (non-square) lattice:
    i_grid, j_grid = np.meshgrid(n0, n1, indexing="ij")
    X_O = a * i_grid
    Y_O=a*j_grid
    mag_A = np.sqrt(Px_arr**2 + Py_arr**2)
    mag_min = mag_A.min()
    mag_max = mag_A.max()
    # Plot using quiver; the 5th argument is the color array.
    plt.figure(figsize=(90, 60))
    scale=1.2
    # Plot dipoles for sublattice A with a colormap for the magnitude
    qA = plt.quiver(
        X_O, Y_O,
        Px_arr, Py_arr,
        mag_A,
        cmap='viridis',
        scale=scale,
        scale_units='xy',
        angles='xy'
    )
    plt.xlabel("x", fontsize=100)
    plt.ylabel("y", fontsize=100)
    avg_polarization_x_str=np.round(avg_polarization_x,3)
    avg_polarization_y_str=np.round(avg_polarization_y,3)
    plt.title(f"Dipole on each site for T = {TStr}, init_path{init_path}, p={avg_polarization_x_str,avg_polarization_y_str}", fontsize=120)
    plt.axis("equal")
    # Add colorbar from one of the quiver plots and increase number size on the colorbar.
    cbar = plt.colorbar(qA)
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.3g'))
    cbar.ax.tick_params(labelsize=120)
    plt.savefig(dipole_each_site_dir+f"/dipole_each_site_T{TStr}.png")
    plt.close()
tStart=datetime.now()
for k in range(0,len(sortedTFiles)):
    oneTFile=sortedTFiles[k]
    lattice_one_T(oneTFile)
tEnd=datetime.now()
print(f"time: {tEnd-tStart}")