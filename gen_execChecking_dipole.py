from pathlib import Path
from decimal import Decimal, getcontext
import shutil
import numpy as np
import pandas as pd
import os
#this script creates slurm bash files for exec_checking_dipole.py

def format_using_decimal(value, precision=4):
    # Set the precision higher to ensure correct conversion
    getcontext().prec = precision + 2
    # Convert the float to a Decimal with exact precision
    decimal_value = Decimal(str(value))
    # Normalize to remove trailing zeros
    formatted_value = decimal_value.quantize(Decimal(1)) if decimal_value == decimal_value.to_integral() else decimal_value.normalize()
    return str(formatted_value)

outPath="./bashFiles_dipole_exec_checking/"

if os.path.isdir(outPath):
    shutil.rmtree(outPath)


Path(outPath).mkdir(exist_ok=True,parents=True)

N=6 #unit cell number
init_path=0
startingFileIndSuggest=5
T_start=2.5
T_end=5.1
T_step=0.01
number=int((T_end-T_start)/T_step)
TVals=[T_start+T_step*n for n in range(0,number+1)]
TStrAll=[]
chunk_size = 100
chunks = [TVals[i:i + chunk_size] for i in range(0, len(TVals), chunk_size)]


def contents_to_bash(chk_ind,T_ind,chunks):
    TStr=format_using_decimal(chunks[chk_ind][T_ind])
    conf_file_name=f"./dataAll/N{N}/T{TStr}/run_T{TStr}.mc.conf"
    contents=[
        "#!/bin/bash\n",
        "#SBATCH -n 2\n",
        "#SBATCH -N 1\n",
        "#SBATCH -t 0-60:00\n",
        "#SBATCH -p hebhcnormal01\n",
        "#SBATCH --mem=4GB\n",
        f"#SBATCH -o out_exec_checking_dipole_{TStr}.out\n",
        f"#SBATCH -e out_exec_checking_dipole_{TStr}.err\n",
        "cd /public/home/hkust_jwliu_1/liuxi/Document/cppCode/fer_symmetry/effective_H_fer\n",
        f"python3 -u exec_checking_dipole.py {TStr} {N} {startingFileIndSuggest} {init_path}\n"

    ]

    out_chunk=outPath+f"/chunk{chk_ind}/"
    Path(out_chunk).mkdir(exist_ok=True,parents=True)
    outBashName=out_chunk+f"/exec_checking_pol_T{TStr}.sh"
    with open(outBashName,"w+") as fptr:
        fptr.writelines(contents)


for chk_ind in range(0,len(chunks)):
    for T_ind in range(0,len(chunks[chk_ind])):
        contents_to_bash(chk_ind,T_ind,chunks)