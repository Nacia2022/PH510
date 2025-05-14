#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Monte Carlo evaluation of Green's functions.

Class file.

Licensed under the MIT License. See the LICENSE file in the repository for details.

"""
# Import
from mpi4py import MPI
import numpy as np



# Create Monte Carlo class for parallel simulations
class MonteCarlo:
    """Initate class to setup parellel processing for the Monte Carlo.
    
    Class performs random walks from a start position x.
    It reaches a boundary, the results are used to buld Green's function. 

    Get the process rank and the total number of processes.
    """

    def __init__(self, seed=None):
        # Initialize MPI communication
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
        
        
    def rndm_walk(self, grid_size, start_xy, boundary):
        """Estimate Green's function using random walks.
        
        Randomly move around a 2D grid until it hits a boundary.
        
        grid_size: Size N of our 2D grid NxN
        start_xy: Coordinates of start position (x,y)
        boundary: Grid coordinates set as boundary points
        """
        count_walkers = np.zeros((grid_size, grid_size))  # 2D array with zeros to record ammount of point visits
        x, y = start_xy

        # Define edges of grid as boundary
        boundary = [(0, i) for i in range(grid_size)] + [(grid_size - 1, i)for i in range(grid_size)] +\
        [(i, 0) for i in range(grid_size)] + [(i, grid_size - 1)for i in range(grid_size)]
        
        # Random walk until boundary, when boundary reached - end walk
        while (x, y) not in boundary:
            count_walkers[x,y] += 1  # Increment count for visits
            step = self.rng.choice(["up", "down", "left", "right"])  # Use rng for random choice of direction
            if step == "up" and x > 0:
                x -= 1
            elif step == "down" and x < grid_size - 1:
                x += 1
            elif step == "left" and y > 0:
                y-= 1
            elif step == "right" and y < 1:
                y += 1
            
        # Return count map of visited points
        count_walkers[x, y] += 1
        return count_walkers


    def green(self, grid_size, start_xy, n_walkers):
        """Use Monte Carlo walks to estimate Green's function.

        Allocate walkers across MPI processes. Each process runs a part of the walkers.
        Results combined in rank 0.
        Return 2D array accumulated at rank 0 for normalized Green's function.
        """
        #Allocate walkers to processes
        loc_walkers = n_walkers // self.size
        loc_count = np.zeros(grid_size, grid_size)
        
        # 
        for _ in range(loc_walkers):
            loc_count += self.rndm_walk(grid_size, start_xy)
            
        # Combine in rank 0
        tot_count = self.comm.reduce(loc_count, op=MPI.SUM, root=0)
        
        # Return Green's function from rank 0 and nothing from other ranks
        if self.rank == 0:
            green = tot_count / n_walkers
            return green
        return None
            
        
# Relaxation/ Over-relaxarion solver
