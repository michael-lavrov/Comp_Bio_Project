import numpy as np
import random
import pickle
from utils.DataManager import DataManager

INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
DEFAULT_GROWTH_RATE = 1.5
C_WIN = 1
L_WIN = 0
DT = 0.1

def logistic_growth_stochastic_differential_model(pandemic_rate, selection_coeff, pandemic_death_coeff, num_of_generations=100,
                                                  growth_rate=1.5):

    """
    Deterministic differential model for logistic growth - Differential version of the discrete model.
    """

    num_of_pandemics = 0
    steps = int(num_of_generations / DT)
    N_t, N_c, N_l = np.empty(steps), np.empty(steps), np.empty(steps)
    # Initializing the populations:
    N_t[0], N_c[0], N_l[0] = INITIAL_NUM_OF_BIRDS*2, INITIAL_NUM_OF_BIRDS, INITIAL_NUM_OF_BIRDS

    # Calculating population growth
    for i in range(1, steps):
        dN_t = (growth_rate * N_t[i-1] * (CARRYING_CAPACITY - N_t[i-1]) / CARRYING_CAPACITY) * DT

        N_t[i] = N_t[i-1] + dN_t
        N_c[i] = ((1+selection_coeff) * N_c[i-1] / ((1+selection_coeff) * N_c[i-1] + N_l[i-1])) * N_t[i]
        N_l[i] = N_t[i] - N_c[i]

        if random.choices([True, False], weights=[pandemic_rate, 1 - pandemic_rate])[0]:
            num_of_pandemics += 1
            N_c[i] *= (1 - np.random.normal(pandemic_death_coeff, 0.1))

    print(f"Number of pandemics in Stochastic model: {num_of_pandemics}")
    return N_c, N_l






