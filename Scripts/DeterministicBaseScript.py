from utils.DataSaver import mk_dir_for_heatmap, save_single_run, save_heatmap_data
from discrete_model.DetermenisticModel import logistic_growth_model
from utils.PiHawkPlotter import Plotter
import time
import sys
import os
import numpy as np


def run_single_deter_dynamics(dir_path):

    # Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity

    data_for_plot = []
    # Colony birds winning scenario:
    params1 = [0.05, 0.05, 0.5, 0, 1000, 1.5, 3000, 10000]
    colony_birds_1, lone_birds_1 = logistic_growth_model(*(params1[:5]))
    save_single_run(dir_path, params1, [colony_birds_1, lone_birds_1])
    data_for_plot.append(([colony_birds_1, lone_birds_1]))
    # Lone birds winning scenario
    params2 = [0.1, 0.05, 0.5, 0, 1000, 1.5, 3000, 10000]
    colony_birds_2, lone_birds_2 = logistic_growth_model(*(params2[:5]))
    save_single_run(dir_path, params2, [colony_birds_2, lone_birds_2])
    data_for_plot.append(([colony_birds_2, lone_birds_2]))
    # Coexistence scenario
    params3 = [1/14, 0.05, 0.5, 0, 1000, 1.5, 3000, 10000]
    colony_birds_3, lone_birds_3 = logistic_growth_model(*(params3[:5]))
    save_single_run(dir_path, params3, [colony_birds_3, lone_birds_3])
    data_for_plot.append(([colony_birds_3, lone_birds_3]))

    subplot_titles = ('Pandemic rate: 0.05', 'Pandemic rate: 0.1', 'Pandemic rate: 0.071')

    Plotter.plot_scatter_subplots(3, 1, data_for_plot, subplot_titles)


def run_deter_heatmap(dir_path):
    # Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity

    new_path = mk_dir_for_heatmap(dir_path)
    pandemic_rates = np.array([0.0] + [1 / i for i in range(15, 1, -1)])
    death_factors = np.linspace(0, 1, 11)

    mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    for i, rate in enumerate(pandemic_rates):
        for j, factor in enumerate(death_factors):
            colony_birds, lone_birds = logistic_growth_model(rate, 0.05, factor, num_of_generations=1000)
            params = [rate, 0.05, factor, 0, 1000, 1.5, 3000, 10000]
            save_single_run(new_path, params, [colony_birds, lone_birds])
            total_last_100 = colony_birds[900:] + lone_birds[900:]
            mat[i][j] = np.average(colony_birds[900:] / total_last_100)
    Plotter.plot_heatmap(mat, death_factors, pandemic_rates, xaxis_title="Death factor", yaxis_title="Pandemic rate")
    save_heatmap_data(new_path, death_factors, pandemic_rates, mat)


def main():
    # [pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity]

    path = sys.argv[1]
    run_single_deter_dynamics(path)
    run_deter_heatmap(path)


if __name__ == "__main__":
    main()


