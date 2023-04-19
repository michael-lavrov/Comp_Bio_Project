import numpy as np
from discrete_model.DetermenisticModel import run_single_iteration
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000


def stochastic_at_death_factor_model(pandemic_rate, selection_coeff, c_pandemic_death_factor, l_pandemic_death_factor=0,
                          num_of_generations=1000, growth_rate=1.5):
    """
    Simple model that calculates for each generation the number of birds of the two types.
    The growth is according to a predetermined growth rate, and a selection coefficient that favors the colony birds.
    Each pandemic year, the two populations are reduced by a certain death factor which is unique to each population.
    :return: The arrays of the numbers of birds in each generation.
    """

    colony_birds = np.empty(num_of_generations)
    lone_birds = np.empty(num_of_generations)

    colony_birds[0] = INITIAL_NUM_OF_BIRDS
    lone_birds[0] = INITIAL_NUM_OF_BIRDS
    carrying_capacity = CARRYING_CAPACITY

    for i in range(1, num_of_generations):

        run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coeff)

        if i % (1 / pandemic_rate) == 0:
            colony_birds[i] *= np.random.normal((1-c_pandemic_death_factor), 0.1)
            # lone_birds[i] *= np.random.normal((1-l_pandemic_death_factor), 0.1)

    return colony_birds, lone_birds

