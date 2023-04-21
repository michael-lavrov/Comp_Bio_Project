import numpy as np

INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
GROWTH_RATE = 1.5
NUM_OF_GENERATIONS = 1000
L_WIN = 0
C_WIN = 1


def logistic_growth_model(pandemic_rate, selection_coefficient, c_death_factor, l_death_factor=0,
                          num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
                          init_num_of_birds=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY):
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

        run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coefficient)

        if i % (1 / pandemic_rate) == 0:
            colony_birds[i] *= (1 - c_death_factor)
            lone_birds[i] *= (1 - l_death_factor)

    return colony_birds, lone_birds


def logistic_growth_model_wrapper(pandemic_rate, selection_coefficient, pandemic_death_coeff):
    c_birds, l_birds = logistic_growth_model(pandemic_rate, selection_coefficient, pandemic_death_coeff)
    if c_birds[len(c_birds) - 1] < 1:
        return L_WIN
    else:
        return C_WIN


def run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coefficient):
    """
    Performs a single iteration of the model, according to the model equations.
    """
    N_total = colony_birds[i - 1] + lone_birds[i - 1]
    N_total += growth_rate * N_total * (carrying_capacity - N_total) / carrying_capacity

    if colony_birds[i-1] < carrying_capacity * 0.001:
        colony_birds[i] = 0
    else:
        colony_birds[i] = N_total*((1 + selection_coefficient) * colony_birds[i - 1] /
                                   ((1 + selection_coefficient) * colony_birds[i - 1] + lone_birds[i - 1]))

    if lone_birds[i-1] < carrying_capacity * 0.001:
        lone_birds[i] = 0
    else:
        lone_birds[i] = (N_total - colony_birds[i])
