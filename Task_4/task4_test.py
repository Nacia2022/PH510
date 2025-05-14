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
import matplotlib as plt
from task4_code import MonteCarlo

# Plot of Green's functing estimated using Monte Carlo 

def plot_results(phi, green):
    """
    Create plot of Green's function.'
    Parameters
    ----------
    phi : TYPE
        DESCRIPTION.
    green : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots(1, figsize=(12, 6))
    
    pl1 = ax[0].imshow(green, cmap='viridis', origin='lower')
    # ax[0].set_title
    # ax[0].set_xlabel
    # ax[0].set_ylabel
    
    plt.show
    
def main():
    """
    Execute function for Monte Carlo: add parameters, compute and plot.

    Returns
    -------
    None.

    """
    # Parameters
    grid_size = 100  # In cm
    space = 0.001
    n_walkers = 1000
    start_xy = (50, 50)  # Start at center
    
    # Set potentials for boundaries
    boundary_cond = {
        "top": np.full(grid_size, 1.0),  # Return array of grid size, filled with +1V
        "bottom": np.full(grid_size, -1.0),  # Return array of grid size, filled with -1V
        "left": np.full(grid_size, 2.0),  # Return array of grid size, filled with +2V
        "right": np.full(grid_size, 4.0)  # Return array of grid size, filled with +4V
    }
    
    # Zero charge inside grid (f=0)
    grid_charge = np.zeros((grid_size, grid_size))
    
    mc_solver = MonteCarlo(seed=71)
    green_func = mc_solver.green(grid_size, start_xy, n_walkers)
    
    # Ensure only rank 0 makes plot
    if MPI.COM_WORLD.Get_rank() == 0:
        plot_results(green_func)
        
if __name__ == :"__main__"
    main()
    
    
    
    
    
    
    
    