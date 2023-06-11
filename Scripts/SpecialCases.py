from discrete_model.logistic_growth_model import logistic_growth_model
from discrete_model.pandemic_functions import deterministic_pandemic_function, types_shift_model_deter_function
from utils.DataSaver import *
from utils.Plotter import Plotter
from utils.Auxiliary import Params, MODEL_NAMES, Model, PARAM_NAMES, ParamName
import sys
import numpy as np
RESCUE_EFFECT = "rescue_effect"
DETER_STR = "Deterministic"
TYPE_SHIFT_STR = "Type switch"
EXTINCTION_DYNAMICS = "extinction_dynamics"
SHIFT_FACTOR_RNG_COMP = "shift_factor_range_comparison"


def rescue_effect(dir_path: str, params: Params) -> None:
    """
    Comparing the deterministic model to the types shift model. The goal is to show that the types shift can help with
    the survival of the species in an extreme epidemic.
    :param dir_path: The directory in which the data is saved.
    :param params: Parameters for the simulation - the same for both models, only the 'type shift' model uses
    the 'type_shift' parameter.
    """

    # new_dir_path = make_new_dir(dir_path, RESCUE_EFFECT)

    # Deterministic model run
    colony_birds1, lone_birds1 = logistic_growth_model(params, deterministic_pandemic_function)
    # save_single_run(new_dir_path, params, [colony_birds1, lone_birds1], MODEL_NAMES[Model.DETER])

    # Type Shift model run
    colony_birds2, lone_birds2 = logistic_growth_model(params, types_shift_model_deter_function)
    # save_single_run(new_dir_path, params, [colony_birds2, lone_birds2], MODEL_NAMES[Model.TYPE_SHIFT])

    # Making subplots
    data_for_plot = [[colony_birds1, lone_birds1], [colony_birds2, lone_birds2]]
    subplot_titles = (DETER_STR, TYPE_SHIFT_STR)
    Plotter.plot_scatter_subplots(2, 1, data_for_plot, subplot_titles)


def extinction_dynamics(dir_path):
    """
    The goal is to show under which parameter combinations, the population goes extinct, and under which the lone birds
    take over.
    """
    data_for_plots = []
    # new_dir_path = make_new_dir(dir_path, extinction_dynamics)

    # First scenario - extinction
    params1 = Params(pandemic_rate=0.1, selection_coefficient=0.1, c_death_factor=0.8,
                     l_death_factor=0.5, num_of_generations=1000, growth_rate=0.1, init_birds_num=3000,
                     carrying_capacity=10000)
    colony_birds1, lone_birds1 = logistic_growth_model(params1, deterministic_pandemic_function)
    data_for_plots.append([colony_birds1, lone_birds1])
    # save_single_run(new_dir_path, params1, [colony_birds1, lone_birds1], MODEL_NAMES[Model.DETER])

    # Second scenario - Lone birds survive, lone death factor is lower
    params2 = params1.copy()
    params2.l_death_factor = 0.45
    colony_birds2, lone_birds2 = logistic_growth_model(params2, deterministic_pandemic_function)
    data_for_plots.append([colony_birds2, lone_birds2])
    # save_single_run(new_dir_path, params2, [colony_birds2, lone_birds2], MODEL_NAMES[Model.DETER])

    # Third scenario - Lone birds survive, selection coefficient is lower
    params3 = params1.copy()
    params3.selection_coefficient = 0.05
    colony_birds3, lone_birds3 = logistic_growth_model(params3, deterministic_pandemic_function)
    data_for_plots.append([colony_birds3, lone_birds3])
    # save_single_run(new_dir_path, params3, [colony_birds3, lone_birds3], MODEL_NAMES[Model.DETER])

    # Plotting the results
    subplot_titles = ("Extinction", "Lower lone death factor", "Lower selection coefficient")
    Plotter.plot_scatter_subplots(3, 1, data_for_plots, subplot_titles)


def type_shift_comparison(dir_path):
    """
    The goal is to compare different shift factor rates, and to show how it helps the species to survive during
    pandemics.
    """

    shift_factor1, shift_factor2, shift_factor3, shift_factor4 = 0.001, 0.002, 0.005, 0.3

    data_for_plots = []
    # new_dir_path = make_new_dir(dir_path, MODEL_NAMES[Model.TYPE_SHIFT])

    # Scenario 1: Shift factor is too small, brings to extinction.
    params1 = Params(pandemic_rate=0.1, selection_coefficient=0.1, c_death_factor=0.8, l_death_factor=0.5,
                     num_of_generations=1000, growth_rate=0.1, init_birds_num=3000, carrying_capacity=10000,
                     shift_factor=shift_factor1)


    colony_birds1, lone_birds1 = logistic_growth_model(params1, types_shift_model_deter_function)
    data_for_plots.append([colony_birds1, lone_birds1])
    # save_single_run(new_dir_path, params1, [colony_birds1, lone_birds1], MODEL_NAMES[Model.TYPE_SHIFT])

    # Scenario 2: Optimal shift factor
    params2 = params1.copy()
    params2.shift_factor = shift_factor2
    colony_birds2, lone_birds2 = logistic_growth_model(params2, types_shift_model_deter_function)
    data_for_plots.append([colony_birds2, lone_birds2])
    # save_single_run(new_dir_path, params2, [colony_birds2, lone_birds2], MODEL_NAMES[Model.TYPE_SHIFT])

    # Scenario 3: Sub-optimal shift factor
    params3 = params1.copy()
    params3.shift_factor = shift_factor3
    colony_birds3, lone_birds3 = logistic_growth_model(params2, types_shift_model_deter_function)
    data_for_plots.append([colony_birds3, lone_birds3])
    # save_single_run(new_dir_path, params3, [colony_birds3, lone_birds3], MODEL_NAMES[Model.TYPE_SHIFT])

    # Scenario 4: Shift factor permits the birds to barely survive
    params4 = params1.copy()
    params4.shift_factor = shift_factor4
    colony_birds4, lone_birds4 = logistic_growth_model(params4, types_shift_model_deter_function)
    data_for_plots.append([colony_birds4, lone_birds4])
    # save_single_run(new_dir_path, params4, [colony_birds4, lone_birds4], MODEL_NAMES[Model.TYPE_SHIFT])

    subplot_titles = (f"{PARAM_NAMES[ParamName.SHIFT_FACTOR]}: {shift_factor1}",
                      f"{PARAM_NAMES[ParamName.SHIFT_FACTOR]}: {shift_factor2}",
                      f"{PARAM_NAMES[ParamName.SHIFT_FACTOR]}: {shift_factor3}",
                      f"{PARAM_NAMES[ParamName.SHIFT_FACTOR]} : {shift_factor4}")
    Plotter.plot_scatter_subplots(4, 1, data_for_plots, subplot_titles)


def shift_factor_range_comparison(dir_path):
    """
    The goal is to inspect a range of shift factors - to examine the average number of total birds for the last
    100 generations, for each shift factor.
    """
    shift_factors = np.linspace(0, 0.1, 101)
    avg_bird_numbers = []

    params = Params(pandemic_rate=0.1, selection_coefficient=0.1, c_death_factor=0.8, l_death_factor=0.48,
                    num_of_generations=1000, growth_rate=0.1, init_birds_num=3000, carrying_capacity=10000)

    # new_dir_path = make_new_dir(dir_path, SHIFT_FACTOR_RNG_COMP)

    for shift_factor in shift_factors:

        params.shift_factor = shift_factor
        colony_birds, lone_birds = logistic_growth_model(params, types_shift_model_deter_function)
        # save_single_run(new_dir_path, params, [colony_birds, lone_birds], MODEL_NAMES[Model.TYPE_SHIFT])
        avg_bird_numbers.append(np.average(colony_birds[900:] + lone_birds[900:]))

    Plotter.plot_bar_plot(shift_factors, avg_bird_numbers, PARAM_NAMES[ParamName.SHIFT_FACTOR],
                          "Number of birds", "Type Shift model")


def main():
    path = sys.argv[1]
    rescue_effect(path, Params(pandemic_rate=0.1, selection_coefficient=0.1, c_death_factor=0.8, l_death_factor=0.48,
                    num_of_generations=1000, growth_rate=0.1, init_birds_num=3000, carrying_capacity=10000,
                    shift_factor=0.002))
    # extinction_dynamics(path)
    # type_shift_comparison(path)



if __name__ == "__main__":
    main()


