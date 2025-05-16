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

    def __init__(self, grid_size, n_walks=100000, seed=None):
        self.n = grid_size
        self.n_walks = n_walks

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

        # Probability grid
        self.prob_grid = np.zeros((self.n, self.n))
        self.visits = np.zeros((self.n, self.n))

    def boundary_check(self, x_val, y_val):
        """Check whether walker has reached boundary."""
        return x_val == 0 or y_val == 0 or x_val == self.n-1 or y_val == self.n - 1


    def rndm_walk(self, int_x, int_y):
        """Perform random walks, return probability of encountering boundary.
        
        Randomly move around a 2D grid until it hits a boundary.
        
        grid_size: Size N of our 2D grid NxN
        start_xy: Coordinates of start position (x,y)
        boundary: Grid coordinates set as boundary points
        """
        #Allocate walkers to processes
        loc_walks = self.n_walks // self.size
        n_hits = {(x_val, y_val): 0 for x_val in range(self.n) for y_val in [0, self.n -1]}
        n_hits.update({(x_val, y_val): 0 for y_val in range(self.n) for x_val in [0, self.n -1]})

        for _ in range(loc_walks):
            x_val, y_val = int_x, int_y

            while not self.boundary_check(x_val, y_val):
                self.visits[x_val, y_val] += 1
                # Use rng for random choice of direction
                step = self.rng.choice(["up", "down", "left", "right"])
                if step == "up": x_val += 1
                elif step == "down": x_val -= 1
                elif step == "left": y_val -= 1
                elif step == "right": y_val += 1
            n_hits[(x_val, y_val)] += 1

        tot_n_hits = self.comm.reduce(n_hits, op=MPI.SUM, root=0)
        tot_visits = self.comm.reduce(self.visits, op=MPI.SUM, root=0)

        if self.rank == 0:
            for (x_val, y_val), count in tot_n_hits.items():
                self.prob_grid[x_val, y_val] = count / self.n_walks
            return self.prob_grid, tot_visits
        return None, None


    def green(self, int_x, int_y, space):
        """Use Monte Carlo walks to estimate Green's function."""
        if self.rank == 0:
            prob_grid, visits = self.rndm_walk(int_x, int_y)
            return (space**2 / self.n_walks) * visits
        return None


    def compute_green(self, x_val ,y_val):
        """Compute green's function."""
        return self.green(x_val, y_val, space=1.0)


class Poissan:
    """Class for solver."""

    def __init__(self, length, n_points, seed=None):
        """Initialize."""
        self.l = length
        self.n = n_points
        self.h = self.l / (self.n - 1)
        self.phi = np.zeros((self.n, self.n))
        self.f = np.zeros((self.n, self.n))
        self.fixed_potential = set()
        self.fixed_charge = set()

        self.mc_solver = MonteCarlo(self.n, seed=seed)

    def boundary_cond(self, type_b):
        """Use diffrent types of boundary conditions specified in task4 a-b."""
        if type_b == "uniform":
            self.phi[:, :] = 0
            self.phi[0, :] = 1
            self.phi[-1, :] = 1
            self.phi[:, 0] = 1
            self.phi[:, -1] = 1

        if type_b == "alternating":
            self.phi[:, :] = 0
            self.phi[0, :] = 1
            self.phi[-1, :] = 1
            self.phi[:, 0] = -1
            self.phi[:, -1] = -1

        if type_b == "mixed":
            self.phi[:, :] = 0
            self.phi[0, :] = 2
            self.phi[-1, :] = 0
            self.phi[:, 0] = 2
            self.phi[:, -1] = -4

        else:
            raise ValueError("Invalid condition type")

        for i in range(self.n):
            self.fixed_potential.add((self.n - 1, i))
            self.fixed_potential.add((i, self.n - 1))
            self.fixed_potential.add((0, i))
            self.fixed_potential.add((i, 0))

        return self.phi


    def charge(self, mode):
        """Distribute charge in diffrent modes."""
        x_val, y_val =np.meshgrid(np.linspace(0, self.l, self.n), np.linspace(0, self.l, self.n))

        if mode == "uniform":  # Fill grid with same value everywhere
            self.f[:, :] = 10

        elif mode == "gradient":  # Gradient charge from 1 to 0 (same charge in every row)
            self.f[:, :] = np.linspace(1, 0, self.n)[:, np.newaxis]

        elif mode == "exponential":  # Exponential decay with highest charge in center
            r = np.sqrt((x_val - self.l / 2)**2 + (y_val - self.l / 2)**2)
            self.f[:, :] = np.exp(-2000 * np.abs(r))

        return self.f


    def over_relaxation(self, iters=1000, tol=1e-5):
        """Summarrize."""
        omega = 2 / (1 + np.sin(np.pi / self.n))

        for _ in range(iters):
            max_delta = 0
            for i in range(self.n):
                for j in range(self.n):
                    if (i, j ) in self.fixed_potential:
                        continue
                    neighbor = [self.phi[i + dx, j + dy] for dx, dy in [(-1,0), (1, 0), (0, -1), (0 ,1)]
                                if 0 <= i + dx < self.n and 0 <= j + dy < self.n]

                    new_phi = (0.25 * self.h**2 * self.f[i, j])+ np.mean(neighbor)
                    max_delta = max(max_delta, abs(new_phi - self.phi[i, j]))
                    self.phi[i ,j] = (omega * new_phi) + ((1 - omega) * self.phi[i, j])
            if max_delta < tol:
                break

    def compute_green_fun(self, x_val, y_val):
        """Compuet function."""
        return self.mc_solver.compute_green(x_val, y_val)

    def evaluate_green(self, pt_list):
        """Convert to cm and return results of green's function"""
        convert_cm = lambda cm: int((cm / self.n) * (self.n - 1))
        results = {}
        for x_cm, y_cm in pt_list:
            x_idx = convert_cm(x_cm)
            y_idx = convert_cm(y_cm)
            greens = self.compute_green_fun(x_idx, y_idx)
            if greens is not None:
                val = greens[x_idx, y_idx]
                stdv = np.std(greens)
                results[(x_cm, y_cm)] = (val, stdv)
            return results
