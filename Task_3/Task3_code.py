#!/bin/python3

"""
Created on Mon Mar 3 16:09:34 2025

@author: natalia
"""

# Importing MPI module to eneable parallel processing
# import time
from mpi4py import MPI
import numpy as np
# import sys

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
        # work into separate processes that will run part of the computation.
        # Seed in rng is for reproducability of a random number sequence so we
        # asign a diffrent seed to each MPI process.
        if seed is not None:
            new_seed = seed + self.rank
        else:
            new_seed = None
        # Else for no provided seed - get numpy to generate a radom seed.
        self.rng = np.random.default_rng(new_seed)

        # Generate random numbers
    def gen_ran_num(self, count=5):
        """Generate random numbers."""
        return self.rng.random(count)

    def mc_volume(self, dimensions, sample_num=10000):
        """Estimate volume of hyperspaces with various dimensions."""
        count = 0  # Counter for points in sphere

        # Distribute work amoung number of processes (self.size)
        for _ in range(sample_num // self.size):
            point = self.rng.uniform(-1, 1, dimensions)  # Create a random point in cube of n-dim
            if np.linalg.norm(point) <= 1:  # Distance from center
                count += 1  # If in spphere increase count

        # Reduce results - sum the results from all processes in rank 0 (root process)
        total = self.comm.reduce(count, op=MPI.SUM, root=0)

        # New version for error analysis
        if self.rank == 0:
            volume_frac = total / sample_num
            volume_cube = 2**dimensions
            volume_esti = volume_cube * volume_frac

            # Error propagation
            volume_err = volume_cube * np.sqrt((volume_frac * (1 - volume_frac)) / sample_num)

            return volume_esti, volume_err  # Rank 0 returns estimated volume and error

        return None, None  # Every other rank returns nothing


# This version is old
        # # Rank 0 gets the volume and other ranks return nothing
        # if self.rank == 0:
        #     volume = (2**dimension)*(total/sample_num)
        #     return volume
        # return None

    # Attempt at Gaussian
    # def mc_gauss(self, x0=0, sig=1, dimensions=1, sample_num=10000):
    #     """Get avarage, variance and integral of Gaussian using Monte Carlo."""
    #     tot_integral = 0

    #     # Distribute work amoung number of processes (self.size)
    #     for _ in range(sample_num // self.size):
    #         x =

# Check that the current script is being run directly as the amin program, or
# if it's being imported as a module into another program.
if __name__ == "__main__":
    sim = MonteCarlo(seed=71)

    # Generate the random numbers
    random_num = sim.gen_ran_num()
    # sys.stdout.flush()  # Manually buffer (otherwise it only prints rank 0)
    # print(f"Process {sim.rank}: {random_num}")

    # Loop to print the random numbers for each rank
    for rank in range(sim.size):
        if sim.rank == rank:
            print(f"Process {sim.rank}: {random_num}")
        # Ensure print in order
        MPI.COMM_WORLD.Barrier()

    if sim.rank == 0:
        print("Simulation has started")
        print("Start calculation for volume of hyperspaces:")

    for dims in [2, 3, 4, 5]:
        vol, vol_err = sim.mc_volume(dims)
        if sim.rank == 0:
            print(f"Estimated volume in {dims}D: {vol:.6f} ± {vol_err:.6f}")


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
