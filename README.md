#this project checks ergodic condition of a C4 ferroelectric system under PBC
# the lattice is square!
# there is  (pi\cdot rij)*(pj \cdot rij) term
# |J| is large
# J<0
# interaction energy is perturbation
# the Hamiltonian is effective, with cross terms:
# J/|r12|^2 p1 \cdot p2 + 2J/|r12|^4 (p1\cdot r12)(p2 \cdot r12)
python mk_dir.py, to set coefficients, T, and directories

# T: 
##########################################
To manually perform each step of computations for U
1. python launch_one_run_U.py ./path/to/mc.conf
2. make run_mc
3. ./run_mc ./path/to/cppIn.txt
4. python check_after_one_run_U.py ./path/to/mc.conf  startingFileIndSuggest
5. go to 1, until no more data points are needed

##########################################
To manually perform each step of computations for dipole
1. python launch_one_run_dipole.py ./path/to/mc.conf
2. make run_mc
3. ./run_mc ./path/to/cppIn.txt
4. python check_after_one_run_dipole.py ./path/to/mc.conf  startingFileIndSuggest
5. go to 1, until no more data points are needed

#########################################
To run 1 pass of mc with checking statistics of dipole
1. cmake .
2. make run_mc
3. python exec_checking_dipole.py T N startingFileIndSuggest init_path
4. run 3 until equilibrium
5. python exec_noChecking.py T N
7. After completing computing dipoles, generate dipole values by
   (a). pkl_dipole_data2csv.py N T init_path
8. After completing computing dipoles, generate U by:
   (a). python check_after_one_run_U.py confFileName startingFileIndSuggest
   (b). python data2csv/pkl_U_data2csv.py N T init_path
   
##############################
in separate_pltLattice/
the plots are by init_path for each N, each T


##############################
plot U and C
in plt/
the plots iterate different T for the same N, the same init_path
1. convert csv file of U to average value, for all T
   python compute_U_avg.py N init_path
2. plot U for all T
   python plt_U.py 
3. compute C for all T
   python compute_C.py N init_path 
4. plot C for all T
   python load_csv_plt_C.py N init_path

##############################
plot dipole
in plt/
1. compute average value of dipole (polarization) for all T
   compute absolute value of polarization for all T
   python compute_dipole_avg.py N init_path
2. plot magnitude of polarization
   python load_csv_plt_abs_polarization.py
3. plot dipole over a lattice
   python load_csv_plt_lattice.py