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
from task4_code import relaxation

# Plot of Green's functing estimated using Monte Carlo

def plot_results(phi, green):
    """
    Create plot of Green's function.
    
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

    # plt.show()  # Can be used but not through ThinLinc
    # Have to save plot rather than show when running via jobscript
    plt.savefig("greens.png", dpi=300)
    print("Saved Green's function plot as image.")


def units(x_cm, y_cm, grid_cm, n_val):
    """Perform unit conversion from si to grid indices."""
    leng = grid_cm / n_val  # Grid spacing
    return int(x_cm / leng), int(y_cm / leng)  # Conversion


def run(grid_size, space, start_cm, boundary_cond, charge, n_walkers):
    """
    Use both Green's and relaxation methods to get the voltage at specific points.'

    Parameters
    ----------
    grid_size : TYPE
        DESCRIPTION.
    space : TYPE
        DESCRIPTION.
    start_cm : TYPE
        DESCRIPTION.
    boundary_cond : TYPE
        DESCRIPTION.
    charge : TYPE
        DESCRIPTION.
    n_walkers : TYPE
        DESCRIPTION.

    Returns
    -------
    results : TYPE
        DESCRIPTION.

    """
    grid_cm = 10
    mc_solver = MonteCarlo(seed=71)
    
    results = []
    for x_cm, y_cm in start_cm:
        start_xy = units(x_cm, y_cm, grid_cm, grid_size)
        green_f, stdv = mc_solver.green(grid_size, start_xy, n_walkers)

        if MPI.COMM_WORLD.Get_rank() == 0:
            phi = relaxation(grid_size, space, charge, boundary_cond)
            poten = np.sum(green_f*charge)
            results.append({
                "point": (x_cm, y_cm),
                "potential": poten,
                "standard deviation": stdv,
                "phi": phi,
                "Green's function": green_f
                })

        return results
    
    
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

    mc_solver = MonteCarlo(seed=71)
    green_func = mc_solver.green(grid_size, start_xy, n_walkers)

    # Ensure only rank 0 makes plot
    if MPI.COMM_WORLD.Get_rank() == 0:
        phi = relaxation(grid_size, space, charge, boundary_cond, 1.8, 1000, 1e-5)
        plot_results(green_func, phi)

if __name__ == "__main__":
    main()
