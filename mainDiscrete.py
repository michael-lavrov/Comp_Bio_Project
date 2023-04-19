import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from discrete_model.DetermenisticModel import logistic_growth_model
from discrete_model.StochasticModel2 import stochastic_at_pandemic_rate_model
from utils.PiHawkPlotter import Plotter
from discrete_model.TypesShiftModel import types_shift_model
from discrete_model.StochasticModel1 import stochastic_at_death_factor_model



def compare_stats(stats1, stats2):

    mat = np.empty(shape=(stats1.size, stats2.size))

    for i, stat1 in enumerate(stats1):
        for j, stat2 in enumerate(stats2):
            colony_birds, lone_birds = logistic_growth_model(stat1, 0.05, stat2, num_of_generations=1000)
            total_last_100 = colony_birds[900:] + lone_birds[900:]
            mat[i][j] = np.average(colony_birds[900:] / total_last_100)
    return mat

if __name__ == "__main__":

    pandemic_rates = np.array([0.0] + [1 / i for i in range(15, 1, -1)])
    death_factors = np.linspace(0, 1, 11)
    mat = compare_stats(pandemic_rates, death_factors)
    Plotter.plot_heatmap(mat, death_factors, pandemic_rates, xaxis_title="Death factor", yaxis_title="Pandemic rate")




