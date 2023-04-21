# This script was written by Michael Lavrov (lavrov14798) in April 2023 as a part of Computational Biology
# Project for undergraduates. The project is done under the supervision of Dr. Oren Kolodny.
# This script consists of functions which ran population dynamics for the Stochastic models.
import sys
from utils.DataSaver import mk_dir_for_heatmap, save_single_run, save_heatmap_data, mk_dir_for_stoch_avg, \
    mk_heatmap_header
from discrete_model.StochasticModel1 import stochastic_at_death_factor_model
from utils.PiHawkPlotter import Plotter
import numpy as np
# Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
# growth_rate, initial_num_of_birds, carrying_capacity
MIN_FRAC_FOR_WIN = 0.95
NUM_OF_RUNS = 10
# Values of unchanging parameters
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
GROWTH_RATE = 1.5
NUM_OF_GENERATIONS = 1000
SELECTION_COEFFICIENT = 0.05
LONE_DEATH_FACTOR = 0


def run_stochastic_model_average(num_of_runs, model_func, model_name, params, path):
    """
    Runs the stochastic model 'num_of_runs' times. At each run calculates the average fraction of colony birds
    in the last 100 generations. Then it checks what scenario has occurred: Colony birds overtook, Lone birds
    overtook, Coexistence. It returns the fraction of each of the scenarios from the total number of runs.
    This function is used to run on a single set of parameters.
    """
    colony_wins, lone_wins, coexist_wins = 0, 0, 0
    new_dir_path = mk_dir_for_stoch_avg(path, params, model_name)

    for i in range(num_of_runs):
        colony_birds, lone_birds = model_func(*params)
        save_single_run(new_dir_path, params, [colony_birds, lone_birds], model_type="Stochastic1")
        colony_last_100, lone_last_100 = colony_birds[900:], lone_birds[900:]
        total_last_100 = colony_last_100 + lone_last_100
        avg_frac = np.average(colony_last_100 / total_last_100)
        if avg_frac > MIN_FRAC_FOR_WIN:
            colony_wins += 1
        elif avg_frac < (1 - MIN_FRAC_FOR_WIN):
            lone_wins += 1
        else:
            coexist_wins += 1
    return colony_wins / num_of_runs, lone_wins / num_of_runs, coexist_wins / num_of_runs


def run_stoch_heatmaps(num_of_runs, model_func, model_name, pandemic_rates, death_factors, dir_path):

    new_path = mk_dir_for_heatmap(dir_path, "Stochastic_1")

    colony_win_mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    lone_win_mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    coexist_mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    for i, rate in enumerate(pandemic_rates):
        for j, factor in enumerate(death_factors):
            params = [rate, SELECTION_COEFFICIENT, factor, LONE_DEATH_FACTOR, NUM_OF_GENERATIONS, GROWTH_RATE,
                      INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
            colony_win_frac, lone_win_frac, coexist_frac = \
                run_stochastic_model_average(num_of_runs, model_func, model_name, params, new_path)
            colony_win_mat[i][j] = colony_win_frac
            lone_win_mat[i][j] = lone_win_frac
            coexist_mat[i][j] = coexist_frac

    Plotter.plot_heatmap(colony_win_mat, death_factors, pandemic_rates, xaxis_title="Death factor",
                         yaxis_title="Pandemic rate", legend_title="Fraction of colony wins")
    Plotter.plot_heatmap(lone_win_mat, death_factors, pandemic_rates, xaxis_title="Death factor",
                         yaxis_title="Pandemic rate", legend_title="Fraction of lone wins")
    Plotter.plot_heatmap(coexist_mat, death_factors, pandemic_rates, xaxis_title="Death factor",
                         yaxis_title="Pandemic rate", legend_title="Fraction of coexistence")
    mk_heatmap_header(new_path, "Stochastic1", "colony_wins")
    mk_heatmap_header(new_path, "Stochastic1", "lone_wins")
    mk_heatmap_header(new_path, "Stochastic1", "coexistence")
    save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, "colony_wins")
    save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, "lone_wins")
    save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, "coexistence")


def main():

    pandemic_rates = np.array([0.0] + [1 / i for i in range(15, 1, -1)])
    death_factors = np.linspace(0, 1, 11)
    run_stoch_heatmaps(NUM_OF_RUNS, stochastic_at_death_factor_model, "Stochastic 1", pandemic_rates, death_factors,
                       sys.argv[1])


if __name__ == "__main__":
    main()
