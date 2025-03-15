#!/bin/bash

#======================================================
#
# Job script for running a serial job on a single core 
#
#======================================================

#======================================================
# Propogate environment variables to the compute node
#SBATCH --export=ALL
#
# Run in the standard partition (queue)
#SBATCH --partition=teaching-gpu
#
# Specify project account
#SBATCH --account=teaching
#
# No. of tasks required (ntasks=1 for a single-core job)
#SBATCH --ntasks=1
#
# Specify (hard) runtime (HH:MM:SS)
#SBATCH --time=00:20:00
#
# Job name
#SBATCH --job-name=Task1
#
# Output file
#SBATCH --output=Task3-%j.out
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
pylint --extension-pkg-allow-list=mpi4py.MPI task3_code.py

# Modify the line below to run your program
mpirun -np $SLURM_NPROCS ./task3_code.py

#======================================================
# Epilogue script to record job endtime and runtime
# Do not change the line below
#======================================================
/opt/software/scripts/job_epilogue.sh 
#------------------------------------------------------
