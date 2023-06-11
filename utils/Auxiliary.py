from dataclasses import dataclass
from enum import Enum
import numpy as np


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
class BirdsPopulations:
    """
    A data class that contains the birds population in each generation.
    Consists of two arrays - one for the colony birds, and one for the lone birds.
    """
    colony_birds: np.ndarray
    lone_birds: np.ndarray

    def get_total_birds_num(self):
        return self.colony_birds + self.lone_birds

    def get_frac_of_colony_birds(self):
        return self.colony_birds / self.get_total_birds_num()

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

    def copy(self):
        return Params(self.pandemic_rate, self.c_death_factor, self.selection_coefficient, self.l_death_factor,
                      self.num_of_generations, self.growth_rate, self.init_birds_num, self.carrying_capacity,
                      self.shift_factor)

    def write_to_file(self, file_path):

        with open(file_path, 'a') as f:
            f.write("Parameters:\n")
            f.write(f"{PARAM_NAMES[ParamName.PANDEMIC_RATE]}: {self.pandemic_rate}\n"
                    f"{PARAM_NAMES[ParamName.C_DEATH_FACTOR]}: {self.c_death_factor}\n"
                    f"{PARAM_NAMES[ParamName.L_DEATH_FACTOR]}: {self.l_death_factor}\n"
                    f"{PARAM_NAMES[ParamName.NUM_OF_GENERATIONS]}: {self.num_of_generations}\n"
                    f"{PARAM_NAMES[ParamName.GROWTH_RATE]}: {self.growth_rate}\n"
                    f"{PARAM_NAMES[ParamName.INIT_BIRDS_NUM]}: {self.init_birds_num}\n"
                    f"{PARAM_NAMES[ParamName.CARRYING_CAPACITY]}: {self.carrying_capacity}\n"
                    f"{PARAM_NAMES[ParamName.SHIFT_FACTOR]}: {self.shift_factor}\n")


MODEL_NAMES = {Model.DETER: "Deterministic_model", Model.STOCHASTIC1: "Stochastic1_model",
               Model.STOCHASTIC2: "Stochastic2_model", Model.STOCHASTIC3: "Stochastic3_model",
               Model.TYPE_SHIFT: "Type_shift_model"}

PARAM_NAMES = {ParamName.PANDEMIC_RATE: "Pandemic rate", ParamName.C_DEATH_FACTOR: "Colony death factor",
               ParamName.SELECTION_COEFFICIENT: "Selection coefficient", ParamName.L_DEATH_FACTOR: "Lone death factor",
               ParamName.NUM_OF_GENERATIONS: "Number of generations", ParamName.GROWTH_RATE: "Growth rate",
               ParamName.INIT_BIRDS_NUM: "Initial number of birds", ParamName.CARRYING_CAPACITY: "Carrying capacity",
               ParamName.SHIFT_FACTOR: "Shift factor"}
