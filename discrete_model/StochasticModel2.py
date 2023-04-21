from discrete_model.DetermenisticModel import run_single_iteration
import numpy as np
import random
from utils.DataManager import DataManager
import pickle

INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
DEFAULT_GROWTH_RATE = 1.5
C_WIN = 1
L_WIN = 0


def stochastic_at_pandemic_rate_model(pandemic_prob, selection_coefficient, c_pandemic_death_factor,
                                      l_pandemic_death_factor=0, num_of_generations=1000, growth_rate=1.5,
                                      init_num_of_birds=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY):
    """
    Stochastic logistic growth model. The stochasticity is in the pandemic rate variable. The pandemic rate is
    the probability of having a pandemic each year.
    """
    colony_birds = []
    lone_birds = []

    # data_manager = DataManager(pandemic_prob, selection_coefficient, c_pandemic_death_factor)
    colony_birds.append(init_num_of_birds)
    lone_birds.append(init_num_of_birds)

    for i in range(num_of_generations):

        run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coefficient)
        # data_manager.generate_seed()
        if random.choices([True, False], weights=[pandemic_prob, 1 - pandemic_prob])[0]:
            colony_birds[i] *= (1 - c_pandemic_death_factor)
            lone_birds[i] *= (1 - l_pandemic_death_factor)

    # DataManager.save_data_manager_obj(data_manager)
    return colony_birds, lone_birds


def stochastic_logistic_growth_model_win_wrapper(pandemic_prob, selection_coefficient, pandemic_death_coeff):
    """
    Uses the data from the stochastic logistic growth model to determine which type took over the population.
    :param pandemic_prob: The chance by which each year a pandemic hits.
    :param selection_coefficient: The selection coefficient that favors the gathering bird growth.
    :param pandemic_death_coeff: The average percentage of birds that die during a pandemic year.
    :return: 1 if the lone birds go extinct, 0 otherwise.
    """
    c_birds, l_birds = stochastic_at_pandemic_rate_model(pandemic_prob, selection_coefficient, pandemic_death_coeff,
                                                         None)
    if c_birds[len(c_birds) - 1] < 1:
        return L_WIN
    else:
        return C_WIN


def calculate_average_wins(number_of_trials, pandemic_probabilities, selection_coeff, pandemic_death_coeff):
    """
    Calculates the average fraction of wins of the gathering birds over a range of pandemic chances.
    :param pandemic_death_coeff: The fraction of birds left alive after a pandemic.
    :param selection_coeff: The coefficient which represents the advantage for the colony birds.
    :param number_of_trials: The number of trails to run for each probability.
    :param pandemic_probabilities: The probabilities for which to run the trial.
    :return: An array that contains the average fractions.
    """
    wins_fraction_arr = []
    for prob in pandemic_probabilities:
        count = 0
        for _ in range(number_of_trials):
            count += stochastic_logistic_growth_model_win_wrapper\
                (prob, selection_coeff, pandemic_death_coeff)
        wins_fraction_arr.append(count / number_of_trials)

    return wins_fraction_arr


def run_stochastic_model_from_seed(seed_saver_path):
    """
    Runs the model using a DataManager object which saves the data of a previous simulation.
    :param seed_saver_path: File path to the DataManager object
    """

    colony_birds = []
    lone_birds = []
    colony_birds.append(INITIAL_NUM_OF_BIRDS)
    lone_birds.append(INITIAL_NUM_OF_BIRDS)
    carrying_capacity = CARRYING_CAPACITY
    growth_rate = DEFAULT_GROWTH_RATE

    with open(seed_saver_path, 'rb') as file:
        data_manager: DataManager = pickle.load(file)

    seeds = data_manager.get_seeds()
    selection_coefficient = data_manager.get_selection_coefficient()
    pandemic_prob = data_manager.get_pandemic_prob()
    pandemic_death_coeff = data_manager.get_pandemic_death_coeff()

    for i in range(len(seeds)):

        run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coefficient)
        random.seed(seeds[i])
        np.random.seed(seeds[i])
        if random.choices([True, False], weights=[pandemic_prob, 1 - pandemic_prob])[0]:
            colony_birds[i+1] *= np.random.normal((1-pandemic_death_coeff), 0.1)

    return colony_birds, lone_birds
