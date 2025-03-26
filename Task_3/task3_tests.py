#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:07:16 2025

@author: natalia

Licensed and Copyrighted 2025.

"""

from mpi4py import MPI
import task3_code as mc

if __name__ == "__main__":
    sim = mc.MonteCarlo(seed=71)

    # Generate the random numbers
    #random_num = sim.gen_ran_num()
    
    # Loop to print the random numbers for each rank
    #for rank in range(sim.size):
    #    if sim.rank == rank:
    #        print(f"Process {sim.rank}: {random_num}")
        # Ensure print in order
    #    MPI.COMM_WORLD.Barrier()

    if sim.rank == 0:
        print("Simulation has started")
        print("Start calculation for volume of hyperspaces:")

    for dims in [2, 3, 4, 5]:
        vol, vol_err = sim.mc_volume(dims)
        if sim.rank == 0:
            print(f"Estimated volume in {dims}D: {vol:.6f} error: {vol_err:.6f}")


# Gaussian Tests

# Define cases for 1D
case_1 = (1, 0.5, 0)
case_2 = (1, 1, -2)
case_3 = (1, 2, 3)

# Define cases for 6D
case_4 = (6, 0.5, 0)
case_5 = (6, 1, -2)
case_6 = (6, 2, 3)

# Sample size for integration
# sample_num = 100000


# Function for gaussian integration using defined cases
def test_gauss(cases):
    """Print results of test."""
    mc_gauss = mc.MonteCarlo(seed=71)
    
    for dimensions, sig, x_0, in cases:
        integral, mean, variance, gauss_err = mc_gauss.gauss_int(x_0=x_0, sig=sig, dimensions=dimensions, sample_num=sample_num)
        
        if mc_gauss.rank == 0:
            if dimensions == 1:
                print(f"1D Test - Integral: {integral:.6f}, Mean: {mean}, Variance: {variance}, Error: {gauss_err:.6f}, Sigma: {sig}, x0: {x_0}")
            else:
                print(f"6D Test - Integral: {integral:.6f}, Mean: {mean}, Variance: {variance}, Error: {gauss_err:.6f}, Sigma: {sig}, x0: {x_0}")

if __name__ == "__main__":
    test_gauss([case_1, case_2, case_3])
    
    test_gauss([case_4, case_5, case_6])



