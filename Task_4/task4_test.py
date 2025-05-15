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
import matplotlib.pyplot as plt
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    pl1 = ax1.imshow(green, cmap='viridis', origin='lower')
    ax1.set_title("Green's Function")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    
    pl2 = ax2.imshow(phi, cmap='viridis', origin='lower')
    # ax[0].set_title
    # ax[0].set_xlabel
    # ax[0].set_ylabel
    
    plt.show()
    

def units(x_cm, y_cm, grid_cm, N):
    """Perform unit conversion from si to grid indices."""
    leng = grid_cm / N  # Grid spacing
    return int(x_cm / leng), int(y_cm / leng)  # Conversion
    
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
    charge = np.zeros((grid_size, grid_size))
    
    mc = MonteCarlo(seed=71)
    green_func = mc.green(grid_size, start_xy, n_walkers)
    
    # Ensure only rank 0 makes plot
    if MPI.COMM_WORLD.Get_rank() == 0:
        phi = mc.relaxation(grid_size, space, charge, boundary_cond)
        plot_results(green_func, phi)
        
if __name__ == "__main__":
    main()

    
    
    
    
    
    