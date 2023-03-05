from PiHawkPlotter import Plotter
from DeterministicModel import logistic_growth_differential_model
from StochasticModel import logistic_growth_stochastic_differential_model
import numpy as np

PANDEMIC_RATE_IND, SELECTION_COEFF_IND, GROWTH_RATE_IND, DEATH_COEFF_IND = 0, 1, 2, 3

DEATH_RATE = 0.5
NUM_OF_TRIALS = 100
NUM_OF_GENERATIONS = 1000
SELECTION_COEFF = 0.05
PANDEMIC_RATE = 0.071
DT = 0.1


def compare_selection_coeffs_and_pandemic_rate(model, num_of_trails, pandemic_rates, selection_coeffs):
    """
    Running a given model with different parameters of pandemic rates and selection coefficients.
    Each pair of parameters is run 'num_of_trials' times. For each pair the fraction of colony birds
    wins is calculated.
    :return: A matrix of pandemic_rates X selection_coeffs where each entry is the fraction of wins of colony birds
    for the pair of parameters.
    """
    mat = np.empty(shape=(selection_coeffs.size, pandemic_rates.size))

    for i, select_coeff in enumerate(selection_coeffs):
        for j, rate in enumerate(pandemic_rates):

            mat[i][j] = get_frac_of_wins(model, num_of_trails, rate, select_coeff)

    return mat


def get_frac_of_wins(model, num_of_trials, pandemic_rate, selection_coeff):
    """
    Gets the fraction of wins of the colony birds of a given model from number_of_trials simulations.
    :return: A float between 0 and 1.
    """
    count = 0
    for _ in range(num_of_trials):
        count += model(pandemic_rate, selection_coeff, DEATH_RATE)

    return count / num_of_trials


def evaluate_parameter(parameter_ind, values, num_of_generations):
    """
    Calculates the fraction of the colony birds from the total population as a function of the specified parameter.
    The calculation is done on a range of values. Each value is ran a 'num_of_generations' times.
    :return: Array of the fractions.
    """
    pandemic_rate, selection_coefficient = PANDEMIC_RATE, SELECTION_COEFF
    fractions = []
    for value in values:

        if parameter_ind == PANDEMIC_RATE_IND:
            colony_birds, lone_birds = logistic_growth_differential_model(value, selection_coefficient,
                                                                          DEATH_RATE, num_of_generations)
        if parameter_ind == SELECTION_COEFF_IND:
            colony_birds, lone_birds = logistic_growth_differential_model(pandemic_rate, value,
                                                                          DEATH_RATE, num_of_generations)
        if parameter_ind == GROWTH_RATE_IND:
            colony_birds, lone_birds = logistic_growth_differential_model(0.069, 0.0489,
                                                                          DEATH_RATE, num_of_generations, value)
        if parameter_ind == DEATH_COEFF_IND:
            colony_birds, lone_birds = logistic_growth_differential_model(0.069, 0.0489,
                                                                          value, num_of_generations)


        total = colony_birds[len(colony_birds) - 1] + lone_birds[len(lone_birds) - 1]
        fractions.append(colony_birds[len(colony_birds) - 1] / total)

    return fractions

def compare_stats(rates, selection_coefficients):

    mat = np.empty(shape=(rates.size, selection_coefficients.size))

    for i, rate in enumerate(rates):
        for j, coeff in enumerate(selection_coefficients):
            colony_birds, lone_birds = logistic_growth_differential_model(rate, coeff, 0.5, 1000)
            total = colony_birds[len(colony_birds)-1] + lone_birds[len(lone_birds) - 1]
            mat[i][j] = colony_birds[len(colony_birds)-1] / total
            if abs(mat[i][j] - 0.5) < 0.1:
                print(rate, "\t", coeff)

    return mat


def comp_average_stochastic_run(num_of_runs, pandemic_rate, selection_coeff, pandemic_death_coeff, num_of_generations=100, growth_rate=1.5):

    sum_colony = np.zeros(int(num_of_generations / DT))
    sum_lone = np.zeros(int(num_of_generations / DT))

    for i in range(num_of_runs):
        colony_birds, lone_birds = logistic_growth_stochastic_differential_model(pandemic_rate, selection_coeff,
                                                                                 pandemic_death_coeff,
                                                                                 num_of_generations, growth_rate)
        sum_colony += colony_birds
        sum_lone += lone_birds

    return sum_colony / num_of_runs, sum_lone / num_of_runs


if __name__ == "__main__":

    # colony_birds, lone_birds = logistic_growth_model()
    # Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, "Deterministic")


    # pandemic_rates = np.arange(0.069, 0.072, 0.0001)
    # selection_coefficients = np.arange(0.0485, 0.052, 0.0001)
    # growth_rates = np.arange(0, 10, 0.1)
    # death_rates = np.arange(0.49, 0.51, 0.001)
    # death_rates = np.arange(0, 1, 0.1)

    # fracs = evaluate_parameter_deterministic_model(3, death_rates, 1000)
    # Plotter.plot_average_fraction_of_wins(death_rates, fracs,
    #                                       "Fraction of colony birds as a function of pandemic death rate")


    colony_birds, lone_birds = logistic_growth_stochastic_differential_model(0.071, 0.05, 0.5)
    Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, "Stochastic")

    # colony_birds, lone_birds = logistic_growth_differential_model(0.0705, 0.05, 0.5, 1000)
    # Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, "Deterministic")

    #colony_birds, lone_birds = comp_average_stochastic_run(100, 0.08, 0.05, 0.5)
    #Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, "Stochastic")


    # data = compare_stats(rates, selection_coefficients)
    # Plotter.plot_heatmap_selection_coeff_pandemic_chance(data, rates, selection_coefficients, "Fraction of colony birds")






