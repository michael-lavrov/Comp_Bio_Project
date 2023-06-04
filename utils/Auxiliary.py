from dataclasses import dataclass
from enum import Enum


class Model(Enum):
    DETER = 0
    STOCHASTIC1 = 1
    STOCHASTIC2 = 2
    STOCHASTIC3 = 3
    TYPE_SHIFT = 4


class ParamName(Enum):
    PANDEMIC_RATE = 0
    C_DEATH_FACTOR = 1
    SELECTION_COEFFICIENT = 2
    L_DEATH_FACTOR = 3
    NUM_OF_GENERATIONS = 4
    GROWTH_RATE = 5
    INIT_BIRDS_NUM = 6
    CARRYING_CAPACITY = 7
    SHIFT_FACTOR = 8

@dataclass
class Params:
    """
    A dataclass that contains all the parameters for a simulation of the models.
    """
    pandemic_rate: float
    c_death_factor: float
    selection_coefficient: float
    l_death_factor: float
    num_of_generations: int
    growth_rate: float
    init_birds_num: int
    carrying_capacity: int
    # Only in types shift model
    shift_factor: float = None


MODEL_NAMES = {Model.DETER: "Deterministic_model", Model.STOCHASTIC1: "Stochastic1_model",
               Model.STOCHASTIC2: "Stochastic2_model", Model.STOCHASTIC3: "Stochastic3_model",
               Model.TYPE_SHIFT: "Type_shift_model"}
PARAM_NAMES = {ParamName.PANDEMIC_RATE: "Pandemic rate", ParamName.C_DEATH_FACTOR: "Colony death factor",
               ParamName.SELECTION_COEFFICIENT: "Selection coefficient", ParamName.L_DEATH_FACTOR: "Lone death factor",
               ParamName.NUM_OF_GENERATIONS: "Number of generations", ParamName.GROWTH_RATE: "Growth rate",
               ParamName.INIT_BIRDS_NUM: "Initial number of birds", ParamName.CARRYING_CAPACITY: "Carrying capacity",
               ParamName.SHIFT_FACTOR: "Shift factor"}
