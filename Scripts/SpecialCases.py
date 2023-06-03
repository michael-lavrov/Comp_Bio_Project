from discrete_model.logistic_growth_model import logistic_growth_model
from discrete_model.types_shift_model import types_shift_model
from utils.DataSaver import *
from utils.Plotter import Plotter
import sys
import numpy as np
SF_IND = 3

def rescue_effect(dir_path):
    """
    Comparing the deterministic model to the types shift model. The goal is to show that the types shift can help with
    the survival of the species in an extreme epidemic.
    """
    # Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity
    pandemic_rate = 0.1
    selection_coefficient = 0.1
    c_death_factor = 0.8
    shift_factor = 0.002
    l_death_factor = 0.48
    num_of_generations = 1000
    growth_rate = 0.1
    init_birds_num = 3000
    carrying_capacity = 10000

    new_dir_path = make_new_dir(dir_path, "RescueEffect")

    # Deterministic model run
    params1 = [pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds1, lone_birds1 = logistic_growth_model()
    save_single_run(new_dir_path, params1, [colony_birds1, lone_birds1], "Deterministic")

    # Type Shift model run
    params2 = [pandemic_rate, selection_coefficient, c_death_factor, shift_factor, l_death_factor, num_of_generations,
               growth_rate, init_birds_num, carrying_capacity]
    colony_birds2, lone_birds2 = types_shift_model(None)
    save_single_run(new_dir_path, params2, [colony_birds2, lone_birds2], "TypeShift")

    # Making subplots
    data_for_plot = [[colony_birds1, lone_birds1], [colony_birds2, lone_birds2]]
    subplot_titles = ("Deterministic", "Type Shift")
    Plotter.plot_scatter_subplots(2, 1, data_for_plot, subplot_titles)


def extinction_dynamics(dir_path):
    """
    The goal is to show under which parameter combinations, the population goes extinct, and under which the lone birds
    take over.
    """
    # Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity
    pandemic_rate = 0.1
    selection_coefficient1, selection_coefficient2 = 0.1, 0.05
    c_death_factor = 0.8
    l_death_factor1, l_death_factor2 = 0.5, 0.45
    num_of_generations = 1000
    growth_rate = 0.1
    init_birds_num = 3000
    carrying_capacity = 10000

    data_for_plots = []
    new_dir_path = make_new_dir(dir_path, "ExtinctionDynamics")

    # First scenario - extinction
    params1 = [pandemic_rate, selection_coefficient1, c_death_factor, l_death_factor1, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds1, lone_birds1 = logistic_growth_model()
    data_for_plots.append([colony_birds1, lone_birds1])
    save_single_run(new_dir_path, params1, [colony_birds1, lone_birds1], "Deterministic")

    # Second scenario - Lone birds survive, lone death factor is lower
    params2 = [pandemic_rate, selection_coefficient1, c_death_factor, l_death_factor2, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds2, lone_birds2 = logistic_growth_model()
    data_for_plots.append([colony_birds2, lone_birds2])
    save_single_run(new_dir_path, params2, [colony_birds2, lone_birds2], "Deterministic")

    # Third scenario - Lone birds survive, selection coefficient is lower
    params3 = [pandemic_rate, selection_coefficient2, c_death_factor, l_death_factor1, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds3, lone_birds3 = logistic_growth_model()
    data_for_plots.append([colony_birds3, lone_birds3])
    save_single_run(new_dir_path, params3, [colony_birds3, lone_birds3], "Deterministic")

    # Plotting the results
    subplot_titles = ("Extinction", "Lower lone death factor", "Lower selection coefficient")
    Plotter.plot_scatter_subplots(3, 1, data_for_plots, subplot_titles)


def lethality_comparison(dir_path):
    """
    The goal is to compare between different types of pandemics which affect the two types of birds in different ways.
    """

    death_factors = [0.8, 0.6, 0.4, 0.2]
    pandemic_rate = 0.1
    selection_coefficient = 0.05
    shift_factor = 0.01
    num_of_generations = 1000
    growth_rate = 0.1
    init_birds_num = 3000
    carrying_capacity = 10000

    data_for_plots = []

    # Scenario 1: Ex
    params1 = [pandemic_rate, selection_coefficient, death_factors[0], death_factors[0], num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds1, lone_birds1 = logistic_growth_model()
    data_for_plots.append([colony_birds1, lone_birds1])


def type_shift_comparison(dir_path):
    """
    The goal is to compare different shift factor rates, and to show how it helps the species to survive during
    pandemics.
    """

    shift_factor1, shift_factor2, shift_factor3, shift_factor4 = 0.001, 0.002, 0.005, 0.3

    pandemic_rate = 0.1
    selection_coefficient = 0.1
    c_death_factor = 0.8
    l_death_factor = 0.48
    num_of_generations = 1000
    growth_rate = 0.1
    init_birds_num = 3000
    carrying_capacity = 10000

    data_for_plots = []
    new_dir_path = make_new_dir(dir_path, "TypeShiftComparison")

    # Scenario 1: Shift factor is too small, brings to extinction.
    params1 = [pandemic_rate, selection_coefficient, c_death_factor, shift_factor1, l_death_factor, num_of_generations,
               growth_rate, init_birds_num, carrying_capacity]
    colony_birds1, lone_birds1 = types_shift_model(None)
    data_for_plots.append([colony_birds1, lone_birds1])
    save_single_run(new_dir_path, params1, [colony_birds1, lone_birds1], "TypeShift")

    # Scenario 2: Optimal shift factor
    params2 = [pandemic_rate, selection_coefficient, c_death_factor, shift_factor2, l_death_factor, num_of_generations,
               growth_rate, init_birds_num, carrying_capacity]
    colony_birds2, lone_birds2 = types_shift_model(None)
    data_for_plots.append([colony_birds2, lone_birds2])
    save_single_run(new_dir_path, params2, [colony_birds2, lone_birds2], "TypeShift")

    # Scenario 3: Sub-optimal shift factor
    params3 = [pandemic_rate, selection_coefficient, c_death_factor, shift_factor3, l_death_factor, num_of_generations,
               growth_rate, init_birds_num, carrying_capacity]
    colony_birds3, lone_birds3 = types_shift_model(None)
    data_for_plots.append([colony_birds3, lone_birds3])
    save_single_run(new_dir_path, params3, [colony_birds3, lone_birds3], "TypeShift")

    # Scenario 4: Shift factor permits the birds to barely survive
    params4 = [pandemic_rate, selection_coefficient, c_death_factor, shift_factor4, l_death_factor, num_of_generations,
               growth_rate, init_birds_num, carrying_capacity]
    colony_birds4, lone_birds4 = types_shift_model(None)
    data_for_plots.append([colony_birds4, lone_birds4])
    save_single_run(new_dir_path, params4, [colony_birds4, lone_birds4], "TypeShift")

    subplot_titles = (f"shift factor: {shift_factor1}", f"shift factor: {shift_factor2}",
                      f"shift factor: {shift_factor3}", f"shift factor : {shift_factor4}")
    Plotter.plot_scatter_subplots(4, 1, data_for_plots, subplot_titles)


def shift_factor_range_comparison(dir_path):
    """
    The goal is to inspect a range of shift factors - to examine the average number of total birds for the last
    100 generations, for each shift factor.
    """
    pandemic_rate = 0.1
    selection_coefficient = 0.1
    c_death_factor = 0.8
    l_death_factor = 0.48
    num_of_generations = 1000
    growth_rate = 0.1
    init_birds_num = 3000
    carrying_capacity = 10000

    shift_factors = np.linspace(0, 0.1, 101)
    avg_bird_numbers = []

    params = [pandemic_rate, selection_coefficient, c_death_factor, 0, l_death_factor,
              num_of_generations, growth_rate, init_birds_num, carrying_capacity]

    new_dir_path = make_new_dir(dir_path, "shift_factor_range_comparison")

    for shift_factor in shift_factors:

        params[SF_IND] = shift_factor
        colony_birds, lone_birds = types_shift_model(None)
        save_single_run(new_dir_path, params, [colony_birds, lone_birds], "TypeShift")
        avg_bird_numbers.append(np.average(colony_birds[900:] + lone_birds[900:]))

    Plotter.plot_bar_plot(shift_factors, avg_bird_numbers, "Shift factor", "Number of birds", "Type Shift model")


def main():
    path = sys.argv[1]
    rescue_effect(path)
    # type_shift_comparison(path)
    # shift_factor_range_comparison(path)


if __name__ == "__main__":
    main()


