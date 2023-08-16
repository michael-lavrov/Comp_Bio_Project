import numpy as np
from utils.Auxiliary import Params
from typing import Callable, Tuple
from discrete_model.logistic_growth_model import run_single_iteration

DT = 1


def logistic_growth_diff(params: Params, pandemic_function: Callable) -> Tuple[np.ndarray, np.ndarray]:

    steps = int(params.num_of_generations // DT)
    colony_birds, lone_birds = np.empty(steps), np.empty(steps)
    colony_birds[0], lone_birds[0] = params.init_birds_num, params.init_birds_num

    for i in range(1, steps):
        run_single_iteration_diff(colony_birds, lone_birds, i, params)
        pandemic_function(colony_birds, lone_birds, i, params)

        if colony_birds[i] < params.carrying_capacity * 0.001:
            colony_birds[i] = 0

        if lone_birds[i] < params.carrying_capacity * 0.001:
            lone_birds[i] = 0

    return colony_birds, lone_birds


def run_single_iteration_diff(colony_birds: np.ndarray, lone_birds: np.ndarray, i: int, params: Params) -> None:
    """
    Performs a single iteration of the model, according to the model equations.
    """
    N_total = colony_birds[i - 1] + lone_birds[i - 1]
    dN_total = (params.growth_rate * N_total * (params.carrying_capacity - N_total) / params.carrying_capacity) * DT
    N_total += dN_total

    colony_birds[i] = N_total * ((1 + params.selection_coefficient) * colony_birds[i - 1] /
                                 ((1 + params.selection_coefficient) * colony_birds[i - 1] + lone_birds[i - 1]))
    lone_birds[i] = (N_total - colony_birds[i])



    # colony_birds[i] = max(0, colony_birds[i-1] + dN_colony)
    # lone_birds[i] = max(0, lone_birds[i-1] + dN_lone)

    #
