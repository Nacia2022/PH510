#!/bin/python3

"""
Monte Carlo Simulation with MPI for volume estimation and gaussian integration.

Class file.

Licensed under the MIT License. See the LICENSE file in the repository for details.

"""

from mpi4py import MPI
import numpy as np



# Create Monte Carlo class for parallel simulations
class MonteCarlo:
    """Initate class to setup parellel processing for the Monte Carlo.

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

    def gen_ran_num(self, count=5):
        """Generate a list ofrandom numbers."""
        return self.rng.random(count)

    def mc_volume(self, dimensions, sample_num=1000000):
        """Estimate volume of hyperspaces with various dimensions using Monte Carlo sampling."""
        count = 0  # Counter for points in sphere

        # Distribute work amoung number of processes (self.size)
        for _ in range(sample_num // self.size):
            point = self.rng.uniform(-1, 1, dimensions)  # Create a random point in cube of n-dim
            if np.linalg.norm(point) <= 1:  # Distance from center
                count += 1  # If in sphere increase count

        # Reduce results - sum the results from all processes in rank 0 (root process)
        total = self.comm.reduce(count, op=MPI.SUM, root=0)

        # New version for error analysis
        if self.rank == 0:
            volume_frac = total / sample_num
            volume_cube = 2**dimensions
            volume_esti = volume_cube * volume_frac

            # Error propagation
            volume_err = volume_cube * np.sqrt((volume_frac * (1 - volume_frac)) / sample_num)

            return volume_esti, volume_err  # Rank 0 returns estimated volume and error
        return None, None  # Every other rank returns nothing

    # Attempt at Gaussian
    def gauss(self, x_1, x_0, sig):
        """Calculate the value of a Gaussian distribution at a point x.
        
        x: Given point
        x0: Mean of distribution
        sig: Standard deviation
        """
        dimens = x_1.shape[1]  # Number of dimensions
        coef = 1/((2*np.pi*sig**2)**(dimens/2))
        exponential = -np.sum((x_1 - x_0) ** 2, axis=1) / (2*sig**2)
        return coef*np.exp(exponential)

        # return np.exp(-((x_1-x_0)**2) / (2 * sig ** 2))/ (sig*np.sqrt(2*np.pi))


    def gauss_int(self, x_0=0, sig=1, dimensions=1, sample_num=1000000):
        """Get the estimated integral, average, and varience of the Gaussian
        function over a finite domain uing Monte Carlo sampling.
        
        x0: Mean of distribution
        sig: Standard deviation
        dimensions: Number of dimensions
        
        samples: draw samples for MC  from the given range -10 sigma to 10 sigma in given dimension.
        Excluding regions of the function that are effectively 0.
        Parallization to spread samples between ranks.
        """
        x_0 = np.full(dimensions, x_0)  # So that its a vector in dimensions over 1

        #
        samples = self.rng.uniform(-10 * sig, 10 * sig, (sample_num // self.size, dimensions))

        # Evaluate function at sampled point with axis for dimensions over 1.
        values = self.gauss(samples, x_0, sig)

        # Estimation of integral over range. Calculate sum of all functions and functions
        # squared at points.
        local_int = np.sum(values)
        local_mean = np.sum(samples * values[:, np.newaxis], axis=0)  # x*f(x)
        local_mean_sq = np.sum((samples**2) * values[:, np.newaxis], axis=0)  # x**2*f(x))

        # Reduce all sums at rank 0.
        total_int = self.comm.reduce(local_int, op=MPI.SUM, root=0)
        total_mean = self.comm.reduce(local_mean, op=MPI.SUM, root=0)
        total_mean_sq = self.comm.reduce(local_mean_sq, op=MPI.SUM, root=0)
        # total_sq = self.comm.reduce(local_sum_sq, op=MPI.SUM, root=0)

        if self.rank ==0:
            # Volume of region
            vol_reg = (20 * sig) ** dimensions

            integral = (total_int / sample_num) * vol_reg
            mean = np.mean(total_mean / total_int) if total_int !=0 else np.zeros(dimensions)
            variance = np.mean((total_mean_sq / total_int) - (mean ** 2))
            gauss_err = np.sqrt(variance) / np.sqrt(sample_num)
            return integral, mean, variance, gauss_err


        return None, None, None, None
