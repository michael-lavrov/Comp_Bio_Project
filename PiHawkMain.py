from StochasticModel import logistic_growth_stochastic_model, stochastic_logistic_growth_model_win_wrapper
from PiHawkPlotter import Plotter
from DeterministicModel import logistic_growth_model_wrapper, logistic_growth_model, logistic_growth_differential_model
import numpy as np


DEATH_RATE = 0.5
NUM_OF_TRIALS = 100
NUM_OF_GENERATIONS = 1000
SELECTION_COEFF = 0.05
PANDEMIC_RATE = 0.071



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


def evaluate_parameter_deterministic_model(parameter_ind, values, num_of_generations):
    """
    Calculates the fraction of the colony birds from the total population as a function of the specified parameter.
    The calculation is done on a range of values. Each value is ran a 'num_of_generations' times.
    :return: Array of the fractions.
    """
    pandemic_rate, selection_coefficient = PANDEMIC_RATE, SELECTION_COEFF
    fractions = []
    for value in values:

        if parameter_ind == 0:
            colony_birds, lone_birds = logistic_growth_differential_model(value, selection_coefficient,
                                                                          DEATH_RATE, num_of_generations)
        else:
            colony_birds, lone_birds = logistic_growth_differential_model(pandemic_rate, value,
                                                                          DEATH_RATE, num_of_generations)

        total = colony_birds[len(colony_birds) - 1] + lone_birds[len(lone_birds) - 1]
        fractions.append(colony_birds[len(colony_birds) - 1] / total)

    return fractions


if __name__ == "__main__":

    # colony_birds, lone_birds = logistic_growth_model()
    # Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, "Deterministic")


    # rates = np.arange(0.069, 0.072, 0.0001)
    selection_coefficients = np.arange(0.0485, 0.052, 0.0001)


    fracs = evaluate_parameter_deterministic_model(1, selection_coefficients, 1000)
    Plotter.plot_average_fraction_of_wins(selection_coefficients, fracs,
                                          "Fraction of colony birds as a function of selection coefficient")


    # colony_birds, lone_birds = logistic_growth_differential_model(PANDEMIC_RATE, 0.05, 0.5, 100)
    # Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, "Differential")






