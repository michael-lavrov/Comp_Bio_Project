# This script was written by Michael Lavrov (lavrov14798) in March-April 2023 as a part of Computational Biology
# Project for undergraduates. The project is done under the supervision of Dr. Oren Kolodny.
# This script consists of two functions which ran population dynamics for the "Deterministic Model".
from utils.DataSaver import mk_dir_for_heatmap, save_single_run, save_heatmap_data, mk_heatmap_header
from discrete_model.DetermenisticModel import logistic_growth_model
from utils.PiHawkPlotter import Plotter
import sys
import numpy as np
# Constant values of unchanging parameters
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
GROWTH_RATE = 1.5
NUM_OF_GENERATIONS = 1000
# Pandemic rates for the three single run scenarios.
RATE1, RATE2, RATE3 = 0.05, 0.1, 1/14

DETER_MODEL = "Deterministic"

# Values to plot a heatmap of pandemic_rate/death_factor
PANDEMIC_RATES = np.array([0.000001] + [1 / i for i in range(15, 1, -1)])
DEATH_FACTORS = np.linspace(0, 1, 11)


def run_single_deter_dynamics(dir_path):
    # Values for the single deterministic runs of three scenarios: Colony birds win, Lone birds win, Coexistence.
    # Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity
    c_win_params = [RATE1, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
    l_win_params = [RATE2, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
    co_ex_params = [RATE3, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]

    data_for_plot = []
    # Colony birds winning scenario:
    colony_birds_1, lone_birds_1 = logistic_growth_model(*c_win_params)
    save_single_run(dir_path, c_win_params, [colony_birds_1, lone_birds_1], DETER_MODEL)
    data_for_plot.append(([colony_birds_1, lone_birds_1]))
    # Lone birds winning scenario
    colony_birds_2, lone_birds_2 = logistic_growth_model(*l_win_params)
    save_single_run(dir_path, l_win_params, [colony_birds_2, lone_birds_2], DETER_MODEL)
    data_for_plot.append(([colony_birds_2, lone_birds_2]))
    # Coexistence scenario
    colony_birds_3, lone_birds_3 = logistic_growth_model(*co_ex_params)
    save_single_run(dir_path, co_ex_params, [colony_birds_3, lone_birds_3], DETER_MODEL)
    data_for_plot.append(([colony_birds_3, lone_birds_3]))

    subplot_titles = (f'Pandemic rate: {RATE1}', f'Pandemic rate: {RATE2}', f'Pandemic rate: {round(RATE3, 5)}')

    Plotter.plot_scatter_subplots(3, 1, data_for_plot, subplot_titles)


def run_deter_heatmap(dir_path):
    # Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity

    new_path = mk_dir_for_heatmap(dir_path, model_name="Deterministic")

    mat = np.empty(shape=(PANDEMIC_RATES.size, DEATH_FACTORS.size))
    for i, rate in enumerate(PANDEMIC_RATES):
        for j, factor in enumerate(DEATH_FACTORS):
            colony_birds, lone_birds = logistic_growth_model(rate, 0.05, factor, num_of_generations=NUM_OF_GENERATIONS)
            params = [rate, 0.05, factor, 0, 1000, 1.5, 3000, 10000]
            save_single_run(new_path, params, [colony_birds, lone_birds], DETER_MODEL)
            total_last_100 = colony_birds[900:] + lone_birds[900:]
            mat[i][j] = np.average(colony_birds[900:] / total_last_100)
    Plotter.plot_heatmap(mat, DEATH_FACTORS, PANDEMIC_RATES, xaxis_title="Death factor", yaxis_title="Pandemic rate")
    mk_heatmap_header(new_path, DETER_MODEL, "colony_birds")
    save_heatmap_data(new_path, DEATH_FACTORS, PANDEMIC_RATES, mat)


def main():
    # [pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity]

    path = sys.argv[1]  # Command line argument for the directory in which to save the data of the runs.
    run_single_deter_dynamics(path)
    run_deter_heatmap(path)


if __name__ == "__main__":
    main()


