from dataclasses import dataclass


@dataclass
class Params:
    # Parameters order: pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,
    # growth_rate, initial_num_of_birds, carrying_capacity
    pandemic_rate: float
    c_death_factor: float
    selection_coefficient: float = 0.05
    l_death_factor: float = 0
    num_of_generations: int = 1000
    growth_rate: float = 1.5
    init_birds_num: int = 3000
    carrying_capacity: int = 10000
