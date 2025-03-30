#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monte Carlo Simulation with MPI for volume estimation and gaussian integration.
Tests file.

Licensed under the MIT License. See the LICENSE file in the repository for details.

"""
import time
from mpi4py import MPI
import task3_code as mc


time1 = time.time()

if __name__ == "__main__":
    # Start time
    time1 = time.time()

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
        print("Start calculation for volume of hyperspaces:")

    for dims in [2, 3, 4, 5]:
        vol, vol_err = sim.mc_volume(dims)
        if sim.rank == 0:
            print(f"Estimated volume in {dims}D: {vol:.6f} error: {vol_err:.6f}")
    # End time
    time2 = time.time()
    # Claculate total time
    total_time1 = time2 - time1
    if sim.rank == 0:
        print(f"Total time for N-ball Volume: {total_time1:.6f} seconds\n")


# Gaussian Tests
def test_gauss():
    """Print results of test."""
    mc_gauss = mc.MonteCarlo(seed=71)

    # Define parameteres
    dim_vals = [1, 6]
    sig_vals = [0.5, 2]
    x_0_vals = [0, 3]
    sample_num = 1000000  # This can be increased for better accuracy

    results = []

    for dimensions in dim_vals:
        for sig in sig_vals:
            for x_0 in x_0_vals:
                intg, mean, var, err = mc_gauss.gauss_int(x_0=x_0,
                                       sig=sig, dimensions=dimensions,
                                       sample_num=sample_num)

                if mc_gauss.rank == 0:
                    results.append((dimensions, sig, x_0, intg, mean, var, err))
                    print(f"Dimensions: {dimensions}, Sigma: {sig}, x0: {x_0}")
                    print(f"Integral: {intg:.6f} error: {err:.6f}")
                    print(f"Mean: {mean:.6f}, Variance: {var:.6f}\n")

    return results

if __name__ == "__main__":
    # Start time
    time3 = time.time()

    test_gauss()
    # End time
    time4 = time.time()
    # Claculate total time
    total_time2 = time4 - time3
    if sim.rank == 0:
        print(f"Total time for Gaussian: {total_time2:.6f} seconds")

MPI.Finalize()
