from StochasticModel import logistic_growth_stochastic_model, stochastic_logistic_growth_model_win_wrapper
from PiHawkPlotter import Plotter
from DeterministicModel import logistic_growth_model_wrapper, logistic_growth_model
import numpy as np

# bdika
DEATH_RATE = 0.5
NUM_OF_TRIALS = 100


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


if __name__ == "__main__":

    # colony_birds, lone_birds = logistic_growth_model()
    # Plotter.plot_birds_numbers_scatter_plot(colony_birds, lone_birds, "Deterministic")


    rates = np.arange(0.05, 0.075, 0.001)
    selection_coefficients = np.arange(0.02, 0.06, 0.001)

    data_mat = compare_selection_coeffs_and_pandemic_rate(stochastic_logistic_growth_model_win_wrapper, NUM_OF_TRIALS,
                                                          rates, selection_coefficients)
    Plotter.plot_heatmap_selection_coeff_pandemic_chance(data_mat, rates, selection_coefficients, "Deterministic model")





