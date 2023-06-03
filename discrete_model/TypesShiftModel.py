import numpy as np
from discrete_model.DetermenisticModel import run_single_iteration

INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000


def types_shift_model(pandemic_rate, selection_coeff, c_pandemic_death_factor, shift_factor,
                      l_pandemic_death_factor=0, num_of_generations=1000, growth_rate=1.5,
                      initial_num_of_birds=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY):
    """
    Simple model that calculates for each generation the number of birds of the two types.
    The growth is according to a predetermined growth rate, and a selection coefficient that favors the colony birds.
    Each pandemic year, the two populations are reduced by a certain death factor which is unique to each population.
    :return: The arrays of the numbers of birds in each generation.
    """

    colony_birds = np.empty(num_of_generations)
    lone_birds = np.empty(num_of_generations)

    colony_birds[0] = initial_num_of_birds
    lone_birds[0] = initial_num_of_birds

    for i in range(1, num_of_generations):

        run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coeff)

        if i % (1 / pandemic_rate) == 0:
            colony_birds[i] *= (1 - c_pandemic_death_factor)
            lone_birds[i] *= (1 - l_pandemic_death_factor)

        # Strategy change
        # strategy_change_rate = np.random.normal(strategy_change_rate, 0.01)
        colony_to_lone = colony_birds[i] * shift_factor
        lone_to_colony = lone_birds[i] * shift_factor
        if colony_to_lone >= 1:
            lone_birds[i] += colony_to_lone
            colony_birds[i] -= colony_to_lone
        if lone_to_colony >= 1:
            colony_birds[i] += lone_to_colony
            lone_birds[i] -= lone_to_colony

    return colony_birds, lone_birds


