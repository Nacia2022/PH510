#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Monte Carlo evaluation of Green's functions.

Class file.

Copyright [2025] Natalia Kozioł.
Licensed under the MIT License. See the LICENSE file in the repository for details.

"""
import matplotlib.pyplot as plt
from task4_code2 import MonteCarlo
from task4_code2 import Poissan

def plot(results_d, title):
    """Plots results of Green's function with error bars"""
    points = list(results_d.keys())
    vals = [v[0] for v in results_d.values()]
    errs = [v[1] for v in results_d.values()]
    labels = [f"({x:.1f}, {y:.1f})" for x, y in points]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, vals, yerr=errs, color="blue", edgecolor="black")
    plt.title(title)
    plt.savefig("Green's.png")
    plt.close()


def run(type_b, mode):
    """Function to run simulations."""
    grid_solve = Poissan(0.10, 21, seed=71)
    grid_solve.boundary_cond(type_b)
    grid_solve.charge(mode)

    grid_solve.over_relaxation()

    use_points = [(5, 5), (2.5, 2.5), (0.1, 2.5), (0.1, 0.1)]
    results = grid_solve.evaluate_green(use_points)

    print("Green's Function at points.")
    for point, (val, stdv) in results.items():
        print(f"Green's function at {point}: Value = {val:.4f}, Stnd. Dev. = {stdv:.4f}")

    plot(results, title=f"Boundary:{type_b}, Charge = {mode}")


def main():
    """Run all simulations."""
    boundary_cond = ["uniform", "alternating", "mixed"]
    charge_dist = ["uniform", "gradient", "exponential"]

    for boundary in boundary_cond:
        for charge in charge_dist:
            run(boundary, charge)


if __name__ == "__main__":
    main()
