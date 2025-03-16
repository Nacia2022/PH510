#!/bin/python3

"""
Created on Mon Mar 3 16:09:34 2025

@author: natalia
"""

# Importing MPI module to eneable parallel processing
# import time
from mpi4py import MPI
import numpy as np

# comm = MPI.COMM_WORLD


# Create Monte Carlo class for parallel simulations
class MonteCarlo:
    """Initate class to setup parellel processing for the Monte Carlo.

    Get the process rank and the total number of processes.
    """

    def __init__(self, seed=None):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        # Random number generator (rng) for each process (rank). We split the
        # work into separate processes that will run part of the computation
        # Seed in rng is for reproducability of a random number sequence so we
        # asign a diffrent seed to each MPI process.
        if seed is not None:
            new_seed = seed + self.rank
        else:
            new_seed = None

        self.rng = np.random.default_rng(new_seed)

        # Generate random numbers
    def gen_ran_num(self, count=5):
        """Generate random numbers."""
        return self.rng.random(count)

    def mc_volume(self, dim, sample_num=1000):
        """Estimate volume of hyperspaces with various dimensions."""
        count = 0
        # Distribute work
        for _ in range(sample_num // self.size):
            point = self.rng.uniform(-1, 1, dim)
            if np.linalg.norm(point) <= 1:
                count += 1

        # Reduce results
        total = self.comm.reduce(count, op=MPI.SUM, root=0)
        if self.rank == 0:
            volume = (2**dim)*(total/sample_num)
            return volume
        return None


# Check that the current script is being run directly as the amin program, or
# if it's being imported as a module into another program.
if __name__ == "__main__":
    sim = MonteCarlo(seed=71)

    # Generate the random numbers
    random_num = sim.gen_ran_num()

    print(f"Process {sim.rank}: {random_num}")

    if sim.rank == 0:
        print("Simulation has started")
        print("Start calculation for volume of hyperspaces:")

    for dim in [2, 3, 4, 5]:
        volume = sim.mc_volume(dim)
        if sim.rank == 0:
            print(f"Volume in {dim}D: {volume}")


# rc.fast_reduce = True # This is the default 9
# # Note the lower case for reduce:
# res = comm.reduce(np.asarray([1,2,3]), op=MPI.SUM)

# if comm.Get_rank() == 0:
# print("All done!", res)














# CODE FOR TASK 1
# # Initializing communication in MPI
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()  # Get the process rank
# size = comm.Get_size()  # Get the total number of processes

# # Get the total number of ranks
# nproc = comm.Get_size()

# # The first processor is leader (rank 0), so one fewer available to be a worker
# nworkers = nproc - 1

# # Integral parameters
# N = 100000  # Number of steps for integration
# DEL = 1.0 / N  # Step size
# INT = 0.0  # Integral


# # Define function
# def integrand(x_i):
#     """Program to integrate the function to obtain the value of pi."""
#     return 4.0 / (1.0 + x_i*x_i)

# # NEW VERSION
# # Divide work (N) amoung the ranks so that each calculates a partial sum of the integral
# DIV_N = N // size
# start = rank * DIV_N
# end = start + DIV_N

# time1 = time.time()
# # Divides integral sum
# DIV_INT = 0.0  # Initialize
# for i in range(start, end):
#     x = (i+0.5) *DEL
#     DIV_INT += integrand(x) * DEL

# # Combine all partial sums
# TOTAL_INT = comm.reduce(DIV_INT, op=MPI.SUM, root=0)

# # Print result from rank 0
# if rank == 0:
#     print(f"Integral = {TOTAL_INT:.15f}")

# time2 = time.time()

# time = time2 - time1

# print("Total time (seconds) =", time)

MPI.Finalize()
