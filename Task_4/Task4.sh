#!/bin/bash

#======================================================
#
# Job script for running a job on a single core 
#
#======================================================

#======================================================
# Propogate environment variables to the compute node

#SBATCH --mem=3G
#SBATCH --export=ALL
#
# Run in the standard partition (queue)
#SBATCH --partition=teaching
#
# Specify project account
#SBATCH --account=teaching
#
# No. of tasks required (ntasks=1 for a single-core job)
#SBATCH --ntasks=8
#
# Specify (hard) runtime (HH:MM:SS)
#SBATCH --time=00:20:00
#
# Job name
#SBATCH --job-name=Task4
#
# Output file
#SBATCH --output=Task4-%j.out
#======================================================

module purge

#Example module load command. 
#Load any modules appropriate for your program's requirements

module load fftw/gcc-8.5.0/3.3.10
module load openmpi/gcc-8.5.0/4.1.1

#======================================================
# Prologue script to record job details
# Do not change the line below
#======================================================
/opt/software/scripts/job_prologue.sh  
#------------------------------------------------------

# Add pylint score
pylint --extension-pkg-allow-list=mpi4py.MPI task4_code.py

# Modify the line below to run your program
mpirun -np $SLURM_NPROCS ./task4_test.py
# mpirun -np 4 ./task3_code.py

#======================================================
# Epilogue script to record job endtime and runtime
# Do not change the line below
#======================================================
/opt/software/scripts/job_epilogue.sh 
#------------------------------------------------------
