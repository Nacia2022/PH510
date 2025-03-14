#!/bin/python3

"""
Created on Mon Mar 3 16:09:34 2025

@author: natalia
"""

# Importing MPI module to eneable parallel processing
import time
from mpi4py import MPI, rc
import numpy as np

comm = MPI.COMM_WORLD

rc.fast_reduce = True # This is the default 9
# Note the lower case for reduce:
res = comm.reduce(np.asarray([1,2,3]), op=MPI.SUM)

if comm.Get_rank() == 0:
print("All done!", res)













# Initializing communication in MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Get the process rank
size = comm.Get_size()  # Get the total number of processes

# Get the total number of ranks
nproc = comm.Get_size()

# The first processor is leader (rank 0), so one fewer available to be a worker
nworkers = nproc - 1

# Integral parameters
N = 100000  # Number of steps for integration
DEL = 1.0 / N  # Step size
INT = 0.0  # Integral


# Define function
def integrand(x_i):
    """Program to integrate the function to obtain the value of pi."""
    return 4.0 / (1.0 + x_i*x_i)

# NEW VERSION
# Divide work (N) amoung the ranks so that each calculates a partial sum of the integral
DIV_N = N // size
start = rank * DIV_N
end = start + DIV_N

time1 = time.time()
# Divides integral sum
DIV_INT = 0.0  # Initialize
for i in range(start, end):
    x = (i+0.5) *DEL
    DIV_INT += integrand(x) * DEL

# Combine all partial sums
TOTAL_INT = comm.reduce(DIV_INT, op=MPI.SUM, root=0)

# Print result from rank 0
if rank == 0:
    print(f"Integral = {TOTAL_INT:.15f}")

time2 = time.time()

time = time2 - time1

print("Total time (seconds) =", time)

# MPI.Finalize()
