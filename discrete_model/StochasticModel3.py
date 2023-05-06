import numpy as np
import random
from discrete_model.DetermenisticModel import run_single_iteration
from scipy.stats import truncnorm
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
UPPER_BOUND = 0.1
STD = 0.1


def stochastic_at_both_model(pandemic_rate, selection_coeff, c_pandemic_death_factor, l_pandemic_death_factor=0,
                             num_of_generations=1000, growth_rate=1.5, init_num_of_birds=INITIAL_NUM_OF_BIRDS,
                             carrying_capacity=CARRYING_CAPACITY):
    """
    Simple model that calculates for each generation the number of birds of the two types.
    The growth is according to a predetermined growth rate, and a selection coefficient that favors the colony birds.
    Each pandemic year, the two populations are reduced by a certain death factor which is unique to each population.
    :return: The arrays of the numbers of birds in each generation.
    """

    colony_birds = np.empty(num_of_generations)
    lone_birds = np.empty(num_of_generations)

    colony_birds[0] = init_num_of_birds
    lone_birds[0] = init_num_of_birds

    for i in range(1, num_of_generations):

        run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coeff)
        if random.choices([True, False], weights=[pandemic_rate, 1 - pandemic_rate])[0]:
            death_factor = 1 - c_pandemic_death_factor
            colony_birds[i] *= truncnorm.rvs((UPPER_BOUND - death_factor) / STD, (np.inf - death_factor) / STD,
                                             loc=death_factor, scale=STD)
            if l_pandemic_death_factor > 0:
                death_factor = 1 - l_pandemic_death_factor
                lone_birds[i] *= truncnorm.rvs((UPPER_BOUND - death_factor) / STD, (np.inf - death_factor) / STD,
                                               loc=death_factor, scale=STD)

    return colony_birds, lone_birds

