# This script was written by Michael Lavrov (lavrov14798) in June 2023 as a part of Computational Biology
# Project for undergraduates. The project is done under the supervision of Dr. Oren Kolodny.
# This script consists of two functions which ran population dynamics for the "Deterministic Model".
from utils.DataSaver import mk_dir_for_heatmap, save_single_run, save_heatmap_data, mk_heatmap_header
from discrete_model.logistic_growth_model import logistic_growth_model
from discrete_model.pandemic_functions import deterministic_pandemic_function
from functions_for_script import run_several_scenarios, run_heatmap_pr_df
from utils.Plotter import Plotter
from utils.Auxiliary import Params, Model, MODEL_NAMES, ParamName, PARAM_NAMES
from typing import Tuple, Callable
import sys
import numpy as np
# Constant values of unchanging parameters
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
GROWTH_RATE = 1.5
NUM_OF_GENERATIONS = 1000
DEFAULT_PANDEMIC_RATE = 1/15
DEFAULT_SELECTION_COEFFICIENT = 0.05
DEFAULT_L_DEATH_FACTOR = 0
# Pandemic rates for the three single run scenarios.
RATE1, RATE2, RATE3 = 0.05, 0.1, 1/14
FACTOR1, FACTOR2, FACTOR3 = 0.4, 0.8, 0.52
# String constants
COLONY_BIRDS_STR = "Colony birds"


def death_factors_comparison_script(dir_path):

    c_win_params = Params(pandemic_rate=0.05, selection_coefficient=DEFAULT_SELECTION_COEFFICIENT,
                          c_death_factor=0.5, l_death_factor=DEFAULT_L_DEATH_FACTOR,
                          num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
                          init_birds_num=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY)
    l_win_params = Params(pandemic_rate=0.1, selection_coefficient=DEFAULT_SELECTION_COEFFICIENT,
                          c_death_factor=0.5, l_death_factor=DEFAULT_L_DEATH_FACTOR,
                          num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
                          init_birds_num=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY)
    # co_ex_params = Params(pandemic_rate=DEFAULT_PANDEMIC_RATE, selection_coefficient=DEFAULT_SELECTION_COEFFICIENT,
    #                       c_death_factor=FACTOR3, l_death_factor=DEFAULT_L_DEATH_FACTOR,
    #                       num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
    #                       init_birds_num=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY)
    subplot_titles = (f'{PARAM_NAMES[ParamName.PANDEMIC_RATE]}: {c_win_params.c_death_factor}',
                      f'{PARAM_NAMES[ParamName.PANDEMIC_RATE]}: {l_win_params.c_death_factor}')

    run_several_scenarios(dir_path, deterministic_pandemic_function, subplot_titles, [c_win_params, l_win_params],
                          "Deterministic")


def run_deterministic_heatmap(dir_path):

    params = Params(pandemic_rate=0, c_death_factor=0, selection_coefficient=0.05, l_death_factor=0,
                    num_of_generations=1000, growth_rate=1.5, init_birds_num=3000, carrying_capacity=10000)
    pandemic_rates = np.array([0.000001] + [1 / i for i in range(15, 1, -1)])
    death_factors = np.linspace(0, 1, 15)
    run_heatmap_pr_df(dir_path, pandemic_rates, death_factors, params, deterministic_pandemic_function)


def deterministic_single_run(dir_path):

    params = Params(pandemic_rate=RATE1, selection_coefficient=0.05, c_death_factor=0.5, l_death_factor=0,
                    num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE, init_birds_num=INITIAL_NUM_OF_BIRDS,
                    carrying_capacity=CARRYING_CAPACITY)

    colony_birds, lone_birds = logistic_growth_model(params, deterministic_pandemic_function)
    fig = Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds,
                                                  f"{PARAM_NAMES[ParamName.PANDEMIC_RATE]}: {RATE1}")
    fig.show()


def main():
    path = sys.argv[1]  # Command line argument for the directory in which to save the data of the runs.
    run_deterministic_heatmap(path)



if __name__ == "__main__":
    main()


