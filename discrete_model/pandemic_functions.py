import numpy as np
import random
from utils.Auxiliary import Params
from scipy.stats import truncnorm
from abc import abstractmethod

UPPER_BOUND = 0.1
STD = 0.1


def deterministic_pandemic_function(colony_birds: np.ndarray, lone_birds: np.ndarray, i: int, params: Params) -> None:
    """
    The pandemic function for the deterministic model. Modifies the population sizes at generation i.
    :param colony_birds: Numpy array of the colony birds populations in each generation.
    :param i: Generation number
    :param lone_birds: Numpy array of the lone birds populations in each generation.
    :param params: A dataclass containing all the relevant parameters.
    :return: None
    """
    if i % (1 / params.pandemic_rate) == 0:
        colony_birds[i] *= (1 - params.c_death_factor)
        lone_birds[i] *= (1 - params.l_death_factor)


def stochastic_at_death_factor_pandemic_function(colony_birds: np.ndarray, lone_birds: np.ndarray,
                                                 i: int, params: Params) -> None:
    """
    The pandemic function for the stochastic at death factor model. Modifies the population sizes at generation i.
    :param colony_birds: Numpy array of the colony birds populations in each generation.
    :param i: Generation number
    :param lone_birds: Numpy array of the lone birds populations in each generation.
    :param params: A dataclass containing all the relevant parameters.
    :return: None
    """

    if i % (1 / params.pandemic_rate) == 0:
        death_factor = 1 - params.c_death_factor
        colony_birds[i] *= truncnorm.rvs((UPPER_BOUND - death_factor) / STD, (np.inf - death_factor) / STD,
                                         loc=death_factor, scale=STD)
        if params.l_death_factor > 0:
            death_factor = 1 - params.l_death_factor
            lone_birds[i] *= truncnorm.rvs((UPPER_BOUND - death_factor) / STD, (np.inf - death_factor) / STD,
                                           loc=death_factor, scale=STD)


def stochastic_at_pandemic_rate_pandemic_function(colony_birds: np.ndarray, lone_birds: np.ndarray, i: int,
                                                  params: Params) -> None:
    """
    The pandemic function for the stochastic at pandemic rate model. Modifies the population sizes at generation i.
    :param colony_birds: Numpy array of the colony birds populations in each generation.
    :param i: Generation number
    :param lone_birds: Numpy array of the lone birds populations in each generation.
    :param params: A dataclass containing all the relevant parameters.
    :return: None
    """
    if random.choices([True, False], weights=[params.pandemic_rate, 1 - params.pandemic_rate])[0]:
        colony_birds[i] *= (1 - params.c_death_factor)
        lone_birds[i] *= (1 - params.l_death_factor)


def stochastic_at_both_pandemic_function(colony_birds: np.ndarray, lone_birds: np.ndarray, i: int, params: Params) \
        -> None:
    """
    The pandemic function for the stochastic at pandemic rate and death factor model.
    Modifies the population sizes at generation i.
    :param colony_birds: Numpy array of the colony birds populations in each generation.
    :param i: Generation number
    :param lone_birds: Numpy array of the lone birds populations in each generation.
    :param params: A dataclass containing all the relevant parameters.
    :return: None
    """

    if random.choices([True, False], weights=[params.pandemic_rate, 1 - params.pandemic_rate])[0]:
        death_factor = 1 - params.c_death_factor
        colony_birds[i] *= truncnorm.rvs((UPPER_BOUND - death_factor) / STD, (np.inf - death_factor) / STD,
                                         loc=death_factor, scale=STD)
        if params.l_death_factor > 0:
            death_factor = 1 - params.l_death_factor
            lone_birds[i] *= truncnorm.rvs((UPPER_BOUND - death_factor) / STD, (np.inf - death_factor) / STD,
                                           loc=death_factor, scale=STD)


def types_shift_model_deter_function(colony_birds: np.ndarray, lone_birds: np.ndarray, i: int, params: Params) -> None:
    """
    The progression function of the 'types shift' model. It performs the type shifting, as well as invoking the
    deterministic pandemic function.
    :param colony_birds: Numpy array of the colony birds populations in each generation.
    :param i: Generation number
    :param lone_birds: Numpy array of the lone birds populations in each generation.
    :param params: A dataclass containing all the relevant parameters.
    :return: None
    """
    deterministic_pandemic_function(colony_birds, lone_birds, i, params)

    colony_to_lone = colony_birds[i] * params.shift_factor
    lone_to_colony = lone_birds[i] * params.shift_factor
    if colony_to_lone >= 1:
        lone_birds[i] += colony_to_lone
        colony_birds[i] -= colony_to_lone
    if lone_to_colony >= 1:
        colony_birds[i] += lone_to_colony
        lone_birds[i] -= lone_to_colony
