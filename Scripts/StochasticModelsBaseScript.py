# This script was written by Michael Lavrov (lavrov14798) in April 2023 as a part of Computational Biology
# Project for undergraduates. The project is done under the supervision of Dr. Oren Kolodny.
# This script consists of functions which ran population dynamics for the Stochastic models.
import sys
from utils.DataSaver import mk_dir_for_heatmap, save_single_run, save_heatmap_data, mk_dir_for_stoch_avg, \
    mk_heatmap_header, data_extractor
from discrete_model.StochasticModel1 import stochastic_at_death_factor_model
from discrete_model.StochasticModel2 import stochastic_at_pandemic_rate_model
from discrete_model.StochasticModel3 import stochastic_at_both_model
from utils.PiHawkPlotter import Plotter
import numpy as np
# Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
# growth_rate, initial_num_of_birds, carrying_capacity
MIN_FRAC_FOR_WIN = 0.95
NUM_OF_RUNS = 100
# Values of unchanging parameters
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
GROWTH_RATE = 1.5
NUM_OF_GENERATIONS = 1000
SELECTION_COEFFICIENT = 0.05
LONE_DEATH_FACTOR = 0
# Rates for single dynamics
RATE1, RATE2, RATE3 = 0.05, 0.1, 1/15


def run_single_stoch_dynamics(dir_path, model, model_name):
    c_win_params = [RATE1, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
    l_win_params = [RATE2, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
    co_ex_params = [RATE3, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
    data_for_plot = []
    # Colony birds winning scenario:
    colony_birds_1, lone_birds_1 = model(*c_win_params)
    save_single_run(dir_path, c_win_params, [colony_birds_1, lone_birds_1], model_name)
    data_for_plot.append(([colony_birds_1, lone_birds_1]))
    # Lone birds winning scenario
    colony_birds_2, lone_birds_2 = model(*l_win_params)
    save_single_run(dir_path, l_win_params, [colony_birds_2, lone_birds_2], model_name)
    data_for_plot.append(([colony_birds_2, lone_birds_2]))
    # Coexistence scenario
    colony_birds_3, lone_birds_3 = model(*co_ex_params)
    save_single_run(dir_path, co_ex_params, [colony_birds_3, lone_birds_3], model_name)
    data_for_plot.append(([colony_birds_3, lone_birds_3]))

    subplot_titles = (f'Pandemic rate: {RATE1}', f'Pandemic rate: {RATE2}', f'Pandemic rate: {round(RATE3, 5)}')

    Plotter.plot_scatter_subplots(3, 1, data_for_plot, subplot_titles)


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
        save_single_run(new_dir_path, params, [colony_birds, lone_birds], model_type=model_name)
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

    new_path = mk_dir_for_heatmap(dir_path, model_name)

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

    subplot_titles = ("Fraction of Colony birds", "Fraction of Lone birds", "Fraction of Coexistence")
    param_names = ["Death factor", "Pandemic rate"]
    Plotter.plot_heatmap_subplots(1, 3, [colony_win_mat, lone_win_mat, coexist_mat], [death_factors, pandemic_rates],
                                  subplot_titles, param_names)
    mk_heatmap_header(new_path, model_name, "colony_wins")
    mk_heatmap_header(new_path, model_name, "lone_wins")
    mk_heatmap_header(new_path, model_name, "coexistence")
    save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, "colony_wins")
    save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, "lone_wins")
    save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, "coexistence")


def main():

    # pandemic_rates = np.array([0.00001] + [1 / i for i in range(15, 1, -1)])
    # death_factors = np.linspace(0, 1, 11)
    # pandemic_rates = np.linspace(0, 1, 31)
    # death_factors = np.linspace(0, 1, 31)
    # run_stoch_heatmaps(NUM_OF_RUNS, stochastic_at_both_model, "Stochastic3", pandemic_rates, death_factors,
    #                    sys.argv[1])
    run_single_stoch_dynamics(sys.argv[1], stochastic_at_death_factor_model, "Stochastic1")


if __name__ == "__main__":
    main()
    # colony_wins, death_factors, pandemic_rates = data_extractor(r"C:\Users\Michael\Desktop\Studies\Comp_Bio_Proj\Data\Stochastic_1_2023-05-02_21-05-11-766522\colony_wins_heatmap_data.csv")
    # lone_wins, _, _ = data_extractor(r"C:\Users\Michael\Desktop\Studies\Comp_Bio_Proj\Data\Stochastic_1_2023-05-02_21-05-11-766522\lone_wins_heatmap_data.csv")
    # coexsitence_wins, _, _ = data_extractor(r"C:\Users\Michael\Desktop\Studies\Comp_Bio_Proj\Data\Stochastic_1_2023-05-02_21-05-11-766522\coexistence_heatmap_data.csv")
    # subplot_titles = ("Fraction of Colony birds", "Fraction of Lone birds", "Fraction of Coexistence")
    # param_names = ["Death factor", "Pandemic rate"]
    # Plotter.plot_heatmap_subplots(1, 3, [colony_wins, lone_wins, coexsitence_wins], [death_factors, pandemic_rates],
    #                               subplot_titles, param_names)
