# This script was written by Michael Lavrov (lavrov14798) in April 2023 as a part of Computational Biology
# Project for undergraduates. The project is done under the supervision of Dr. Oren Kolodny.
# This script consists of functions which ran population dynamics for the Stochastic models.
import sys
from discrete_model.logistic_growth_model import logistic_growth_model
from discrete_model.pandemic_functions import stochastic_at_pandemic_rate_pandemic_function
from functions_for_script import run_three_scenarios, run_stoch_heatmaps_pr_df
from utils.DataSaver import mk_dir_for_heatmap, save_single_run, save_heatmap_data, mk_dir_for_stoch_avg, \
    mk_heatmap_header, data_extractor
from utils.Auxiliary import Params, PARAM_NAMES, ParamName
from utils.Plotter import Plotter
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
DEFAULT_L_DEATH_FACTOR = 0
DEFAULT_C_DEATH_FACTOR = 0.5
DEFAULT_SELECTION_COEFFICIENT = 0.05
# Rates for single dynamics
RATE1, RATE2, RATE3 = 0.05, 0.1, 1/15


def pandemic_rates_comparison_script_stoch_model(dir_path):

    c_win_params = Params(pandemic_rate=RATE1, selection_coefficient=DEFAULT_SELECTION_COEFFICIENT,
                          c_death_factor=DEFAULT_C_DEATH_FACTOR, l_death_factor=DEFAULT_L_DEATH_FACTOR,
                          num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
                          init_birds_num=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY)

    l_win_params = Params(pandemic_rate=RATE2, selection_coefficient=DEFAULT_SELECTION_COEFFICIENT,
                          c_death_factor=DEFAULT_C_DEATH_FACTOR, l_death_factor=DEFAULT_L_DEATH_FACTOR,
                          num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
                          init_birds_num=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY)
    co_ex_params = Params(pandemic_rate=RATE3, selection_coefficient=DEFAULT_SELECTION_COEFFICIENT,
                          c_death_factor=DEFAULT_C_DEATH_FACTOR, l_death_factor=DEFAULT_L_DEATH_FACTOR,
                          num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
                          init_birds_num=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY)

    subplot_titles = (f'{PARAM_NAMES[ParamName.C_DEATH_FACTOR]}: {c_win_params.c_death_factor}',
                      f'{PARAM_NAMES[ParamName.C_DEATH_FACTOR]}: {l_win_params.c_death_factor}',
                      f'{PARAM_NAMES[ParamName.C_DEATH_FACTOR]}: {co_ex_params.c_death_factor}')
    run_three_scenarios(dir_path, c_win_params, l_win_params, co_ex_params,
                        stochastic_at_pandemic_rate_pandemic_function, subplot_titles)


def fraction_heatmaps_script(dir_path):

    pandemic_rates = np.array([0.00001] + [1 / i for i in range(15, 1, -1)])
    death_factors = np.linspace(0, 1, 15)
    params = Params(pandemic_rate=0, selection_coefficient=0.05, c_death_factor=0, l_death_factor=0,
                    num_of_generations=1000, init_birds_num=3000, growth_rate=1.5, carrying_capacity=10000)
    run_stoch_heatmaps_pr_df(num_of_runs=10, pandemic_func=stochastic_at_pandemic_rate_pandemic_function,
                             model_name="Stochastic1", pandemic_rates=pandemic_rates, death_factors=death_factors,
                             params=params, dir_path=dir_path)


def run_example_bird_population(dir_path, model, model_name):

    params = [RATE1, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
    colony_birds, lone_birds = model(*params)
    fig = Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, model_name)
    fig.show()


def main():

    # pandemic_rates = np.linspace(0, 1, 11)
    # death_factors = np.linspace(0, 1, 31)
    path = sys.argv[1]
    fraction_heatmaps_script(path)


if __name__ == "__main__":
    main()
