from discrete_model.DetermenisticModel import logistic_growth_model
from discrete_model.TypesShiftModel import types_shift_model
from utils.DataSaver import *
from utils.PiHawkPlotter import Plotter
import sys


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
    shift_factor = 0.01
    l_death_factor = 0.48
    num_of_generations = 1000
    growth_rate = 0.1
    init_birds_num = 3000
    carrying_capacity = 10000

    new_dir_path = make_new_dir(dir_path, "RescueEffect")

    # Deterministic model run
    params1 = [pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds1, lone_birds1 = logistic_growth_model(*params1)
    save_single_run(new_dir_path, params1, [colony_birds1, lone_birds1], "Deterministic")

    # Type Shift model run
    params2 = [pandemic_rate, selection_coefficient, c_death_factor, shift_factor, l_death_factor, num_of_generations,
               growth_rate, init_birds_num, carrying_capacity]
    colony_birds2, lone_birds2 = types_shift_model(*params2)
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
    colony_birds1, lone_birds1 = logistic_growth_model(*params1)
    data_for_plots.append([colony_birds1, lone_birds1])
    save_single_run(new_dir_path, params1, [colony_birds1, lone_birds1], "Deterministic")

    # Second scenario - Lone birds survive, lone death factor is lower
    params2 = [pandemic_rate, selection_coefficient1, c_death_factor, l_death_factor2, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds2, lone_birds2 = logistic_growth_model(*params2)
    data_for_plots.append([colony_birds2, lone_birds2])
    save_single_run(new_dir_path, params2, [colony_birds2, lone_birds2], "Deterministic")

    # Third scenario - Lone birds survive, selection coefficient is lower
    params3 = [pandemic_rate, selection_coefficient2, c_death_factor, l_death_factor1, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds3, lone_birds3 = logistic_growth_model(*params3)
    data_for_plots.append([colony_birds3, lone_birds3])
    save_single_run(new_dir_path, params3, [colony_birds3, lone_birds3], "Deterministic")

    # Plotting the results
    subplot_titles = ("Extinction", "Lower lone death factor", "Lower selection coefficient")
    Plotter.plot_scatter_subplots(3, 1, data_for_plots, subplot_titles)


def lethality_comparison(dir_path):
    """
    The goal is to compare between different types of pandemics which affect the two types in different ways.
    """

    pandemic_rate = 0.1
    selection_coefficient = 0.1
    c_death_factor = 0.8
    shift_factor = 0.01
    l_death_factor = 0.48
    num_of_generations = 1000
    growth_rate = 0.1
    init_birds_num = 3000
    carrying_capacity = 10000

    data_for_plots = []

    params1 = [pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, num_of_generations, growth_rate,
               init_birds_num, carrying_capacity]
    colony_birds1, lone_birds1 = logistic_growth_model(*params1)
    data_for_plots.append([colony_birds1, lone_birds1])


def main():
    path = sys.argv[1]
    # rescue_effect(path)
    extinction_dynamics(path)



if __name__ == "__main__":
    main()


