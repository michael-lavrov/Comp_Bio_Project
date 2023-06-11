import numpy as np
from utils.Auxiliary import Params, BirdsPopulations
from typing import Callable, Tuple


def logistic_growth_model(params: Params, pandemic_function: Callable) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculates the logistic growth each year according to preset parameters. Applies the pandemic function in
    each generation.
    :param params - A dataclass containing all the relevant parameters.
    :param pandemic_function - A function that calculates whether a pandemic hits, and the losses from the pandemic.
    :return colony_birds, lone_birds - Numpy arrays of the population of colony and lone birds in each generation.
    """

    colony_birds, lone_birds = np.empty(params.num_of_generations), np.empty(params.num_of_generations)
    colony_birds[0], lone_birds[0] = params.init_birds_num, params.init_birds_num

    for i in range(1, params.num_of_generations):
        run_single_iteration(colony_birds, lone_birds, i, params)
        pandemic_function(colony_birds, lone_birds, i, params)

    return colony_birds, lone_birds


def run_single_iteration(colony_birds: np.ndarray, lone_birds: np.ndarray, i: int, params: Params) -> None:
    """
    Performs a single iteration of the model, according to the model equations.
    """
    N_total = colony_birds[i - 1] + lone_birds[i - 1]
    N_total += params.growth_rate * N_total * (params.carrying_capacity - N_total) / params.carrying_capacity

    if colony_birds[i - 1] < params.carrying_capacity * 0.001:
        colony_birds[i] = 0
    else:
        colony_birds[i] = N_total * ((1 + params.selection_coefficient) * colony_birds[i - 1] /
                                     ((1 + params.selection_coefficient) * colony_birds[i - 1] + lone_birds[i - 1]))

    if lone_birds[i - 1] < params.carrying_capacity * 0.001:
        lone_birds[i] = 0
    else:
        lone_birds[i] = (N_total - colony_birds[i])
