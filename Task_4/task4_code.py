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
        # 2D array with zeros to record ammount of point visits
        count_walkers = np.zeros((grid_size, grid_size))
        x_val, y_val = start_xy

        # # Define edges of grid as boundary
        # boundary = [(0, i) for i in range(grid_size)] +
        # [(grid_size - 1, i)for i in range(grid_size)] +\
        # [(i, 0) for i in range(grid_size)] + [(i, grid_size - 1)for i in range(grid_size)]

        # Random walk until boundary, when boundary reached - end walk
        while (x_val, y_val) not in boundary:
            count_walkers[x_val, y_val] += 1  # Increment count for visits

            # Use rng for random choice of direction
            step = self.rng.choice(["up", "down", "left", "right"])
            if step == "up" and x_val > 0:
                x_val -= 1
            elif step == "down" and x_val < grid_size - 1:
                x_val += 1
            elif step == "left" and y_val > 0:
                y_val -= 1
            elif step == "right" and y_val < grid_size - 1:
                y_val += 1

        # Return count map of visited points
        count_walkers[x_val, y_val] += 1
        return count_walkers


    def green(self, grid_size, start_xy, n_walkers):
        """Use Monte Carlo walks to estimate Green's function.

        Allocate walkers across MPI processes. Each process runs a part of the walkers.
        Results combined in rank 0.
        Return 2D array accumulated at rank 0 for normalized Green's function.
        """
        #Allocate walkers to processes
        loc_walkers = n_walkers // self.size
        loc_count = np.zeros((grid_size, grid_size))

        # Define edges of grid as boundary
        boundary = [(0, i) for i in range(grid_size)] +\
        [(grid_size - 1, i)for i in range(grid_size)] +\
        [(i, 0) for i in range(grid_size)] +\
        [(i, grid_size - 1)for i in range(grid_size)]


        for _ in range(loc_walkers):
            loc_count += self.rndm_walk(grid_size, start_xy, boundary)

        # Combine in rank 0
        tot_count = self.comm.reduce(loc_count, op=MPI.SUM, root=0)

        # Return Green's function from rank 0 and nothing from other ranks
        if self.rank == 0:
            green = tot_count / n_walkers
            stdv = np.sqrt(green * (1 - green) / n_walkers)
            return green, stdv
        return None, None


# Relaxation/ Over-relaxarion solver
# def relaxation(param):
def relaxation(grid_size, space, charge, boundary_cond, omega=1.8, iters=1000, tol=1e-5):
    """
    Summarrize.
    
    Parameters
    ----------
    grid_size : TYPE
        DESCRIPTION.
    space : TYPE
        DESCRIPTION.
    charge : TYPE
        DESCRIPTION.
    boundary_cond : TYPE
        DESCRIPTION.
    omega : TYPE, optional
        DESCRIPTION. The default is 1.8.
    iters : TYPE, optional
        DESCRIPTION. The default is 1000.
    tol : TYPE, optional
        DESCRIPTION. The default is 1e-5.

    Returns
    -------
    None.

    """
    # grid_size, space, charge, boundary_cond, omega, iters, tol = param
    # omega=1.8
    # iters=1000
    # tol=1e-5

    phi = np.zeros((grid_size, grid_size))

    # Set boundary conditions
    phi[0, :] = boundary_cond["top"]
    phi[-1, :] = boundary_cond["bottom"]
    phi[:, 0] = boundary_cond["left"]
    phi[:, -1] = boundary_cond["right"]

    for _ in range(iters):
        old_phi = phi.copy()
    #
        for i in range(1, grid_size -1):
            for j in range(1, grid_size -1):
                phi[i, j] = omega * (charge[i, j] * space **2 + (phi[i+1, j]+ phi[i-1, j]
                    + phi[i, j+1] + phi[i, j-1])/4) + (1 - omega) * old_phi[i, j]

        # Check
        if np.max(np.abs(phi - old_phi)) < tol:
        # if np.linalg.norm(phi - old_phi) < tol:
            break

    return phi
