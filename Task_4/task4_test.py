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
    ax2.set_title("Phi")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")


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
            poten = np.sum(green_f*charge) * space**2
            results.append({
                "point": (x_cm, y_cm),
                "potential": poten,
                "standard deviation": np.mean(stdv),
                "phi": phi,
                "Green's function": green_f
                })

        return results
    

def charge_dist(grid_size, mode="zero"):
    """
    Define charge distribution across the grid.

    Parameters
    ----------
    grid_size : TYPE
        DESCRIPTION.
    mode : Tell function how to fill grid. The default is "zero".

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if mode == "zero":  # Fill grid with 0s - no charge anywhere
        return np.zeros((grid_size, grid_size))
    elif mode == "uniform":  # Fill grid with same value everywhere
        return np.full((grid_size, grid_size), 10.0 / (grid_size**2))
    elif mode == "gradient":  # Gradient charge from 1 to 0 (same charge in every row)
        return np.title(np.linspace(1, 0, grid_size).reshape((grid_size, 1)), (1, grid_size))
    elif mode == "exponential":  # Exponential decay with highest charge in center
        charge = np.zeros((grid_size, grid_size))
        center = grid_size // 2
        for i in range(grid_size, grid_size):
            for j in range(grid_size):
                r = np.sqrt((i - center) **2 + (j - center)**2)
                charge[i, j] = np.exp(-2000*r / grid_size)
            return charge
    """
    Define charge distribution across the grid.

    Parameters
    ----------
    grid_size : TYPE
        DESCRIPTION.
    mode : Tell function how to fill grid. The default is "zero".

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if mode == "zero":  # Fill grid with 0s - no charge anywhere
        return np.zeros((grid_size, grid_size))
    elif mode == "uniform":  # Fill grid with same value everywhere
        return np.full((grid_size, grid_size), 10.0 / (grid_size**2))
    elif mode == "gradient":  # Gradient charge from 1 to 0 (same charge in every row)
        return np.tile(np.linspace(1, 0, grid_size).reshape((grid_size, 1)), (1, grid_size))
    elif mode == "exponential":  # Exponential decay with highest charge in center
        charge = np.zeros((grid_size, grid_size))
        center = grid_size // 2
        for i in range(grid_size):
            for j in range(grid_size):
                r = np.sqrt((i - center)**2 + (j - center)**2)
                charge[i, j] = np.exp(-2000 * r / grid_size)
            return charge



def main():
    """
    Execute function for Monte Carlo: add parameters, compute and plot.

    Returns
    -------
    None.

    """
    # Parameters
    grid_size = 100  # In cm
    space = 10 / grid_size
    n_walkers = 1000
    # start_xy = (50, 50)  # Start at center
    start_cm = [(5, 5), (2.5, 2.5), (0.1, 2.5), (0.1, 0.1)]

    # Set potentials for boundaries (various)
    boundaries = [
        {"top": np.full(grid_size, 1.0),  # All egdes uniformally at +1V
         "bottom": np.full(grid_size, 1.0),  
         "left": np.full(grid_size, 1.0),  
         "right": np.full(grid_size, 1.0)},

        {"top": np.full(grid_size, 1.0),
         "bottom": np.full(grid_size, 1.0),
         "left": np.full(grid_size, -1.0),
         "right": np.full(grid_size, -1.0)},

        {"top": np.full(grid_size, 2.0),
         "bottom": np.full(grid_size, 0),
         "left": np.full(grid_size, 2.0),
         "right": np.full(grid_size, -4.0)},
    ]
    
    modes = ["zero", "uniform", "gradient", "exponential"]

    # Zero charge inside grid (f=0)
    # charge = np.zeros((grid_size, grid_size))

    # mc_solver = MonteCarlo(seed=71)
    # green_func = mc_solver.green(grid_size, start_xy, n_walkers)

    # if MPI.COMM_WORLD.Get_rank() == 0:
    #     phi = relaxation(grid_size, space, charge, boundary_cond, 1.8, 1000, 1e-5)
    #     plot_results(green_func, phi)
    
    if MPI.COMM_WORLD.Get_rank() == 0:
        for indx_boundary, boundary_cond in enumerate(boundaries):
            for indx_charge, mode in enumerate(modes):
                charge = charge_dist(grid_size, mode)
                results = run(grid_size, space, start_cm, boundary_cond, charge, n_walkers)
                for r in results:
                    print(f"Boundary type: {indx_boundary+1}, Charge {mode}, Point {r['point']}, Potential: {r['potential']:.5f}, Standard deviation: {r['stdv']:.5e}")
        

if __name__ == "__main__":
    main()
