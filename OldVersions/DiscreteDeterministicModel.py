INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
DEFAULT_GROWTH_RATE = 1.5
L_WIN = 0
C_WIN = 1
DT = 0.1


def logistic_growth_model(pandemic_rate, selection_coeff, pandemic_death_coeff, num_of_generations):

    """
    Simple model that calculates for each generation the number of birds of the two types. Plots a graph.
    The growth is according to  a predetermined growth rate, and a selection coefficient that favors the colony birds.
    Each pandemic year, the colonial population is reduced by a certain amount.
    :param pandemic_rate: The rate of pandemics during the simulation. (Each 'pandemic_rate' generations).
    :param selection_coeff: The selection coefficient that favors the gathering bird growth.
    :param pandemic_death_coeff: The coefficient by which te gathering population gets reduced during a pandemic year.
    :param num_of_generations: Number of generations to run the simulation.
    :return: The arrays of the numbers of birds in each generation.
    """

    colony_birds = []
    lone_birds = []

    colony_birds.append(INITIAL_NUM_OF_BIRDS)
    lone_birds.append(INITIAL_NUM_OF_BIRDS)
    carrying_capacity = CARRYING_CAPACITY
    growth_rate = DEFAULT_GROWTH_RATE

    for i in range(num_of_generations):

        run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coeff)

        if i % (1/pandemic_rate) == 0:
            colony_birds[i] *= (1-pandemic_death_coeff)

    return colony_birds, lone_birds


def logistic_growth_model_wrapper(pandemic_rate, selection_coefficient, pandemic_death_coeff):

    c_birds, l_birds = logistic_growth_model(pandemic_rate, selection_coefficient, pandemic_death_coeff, None)
    if c_birds[len(c_birds) - 1] < 1:
        return L_WIN
    else:
        return C_WIN


def run_single_iteration(carrying_capacity, colony_birds, growth_rate, i, lone_birds, selection_coefficient):
    """
    Performs a single iteration of the model, according to the model equations.
    """

    N_total = colony_birds[i] + lone_birds[i]
    N_total = growth_rate * N_total * (carrying_capacity - N_total) / carrying_capacity
    colony_birds.append((1 + selection_coefficient) * colony_birds[i] /
                        ((1 + selection_coefficient) * colony_birds[i] + lone_birds[i]) * N_total)
    lone_birds.append(N_total - colony_birds[i + 1])
