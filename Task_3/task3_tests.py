#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:07:16 2025

@author: natalia

Licensed and Copyrighted 2025.

"""

from mpi4py import MPI
import numpy as np
import MonteCarlo

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

