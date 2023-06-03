import numpy as np
from utils.Auxiliary import Params, ParamName, PARAM_NAMES
from discrete_model.logistic_growth_model import logistic_growth_model
from typing import Tuple, Callable
from utils.Plotter import Plotter
from utils.DataSaver import mk_dir_for_heatmap, make_new_dir, save_heatmap_data, save_single_run
FRAC_OF_COLONY_BIRDS_TITLE = "Fraction of colony birds"


def run_three_scenarios(dir_path: str, first_scenario_params: Params, second_scenario_params: Params,
                        third_scenario_params: Params, pandemic_function: Callable,
                        subplot_titles: Tuple[str, str, str]) -> None:
    """
    A function that runs three different scenarios of a given model. The parameters for the three scenarios
    are passed to the function as arguments separately. The changing variable is determined by the arguments.
    Plots the three scenarios in one image.
    :param dir_path: Path for directory in which to save the data.
    :param first_scenario_params:
    :param second_scenario_params:
    :param third_scenario_params:
    :param pandemic_function: The function that determines the model's behavior during pandemic.
    :param subplot_titles: Titles for the plot subplots.
    :return: None
    """
    data_for_plot = []
    # Colony birds winning scenario:
    colony_birds_1, lone_birds_1 = logistic_growth_model(first_scenario_params, pandemic_function)
    # save_single_run(dir_path, c_win_params, [colony_birds_1, lone_birds_1], DETER_MODEL)
    data_for_plot.append(([colony_birds_1, lone_birds_1]))
    # Lone birds winning scenario
    colony_birds_2, lone_birds_2 = logistic_growth_model(second_scenario_params, pandemic_function)
    # save_single_run(dir_path, l_win_params, [colony_birds_2, lone_birds_2], DETER_MODEL)
    data_for_plot.append(([colony_birds_2, lone_birds_2]))
    # Coexistence scenario
    colony_birds_3, lone_birds_3 = logistic_growth_model(third_scenario_params, pandemic_function)
    # save_single_run(dir_path, co_ex_params, [colony_birds_3, lone_birds_3], DETER_MODEL)
    data_for_plot.append(([colony_birds_3, lone_birds_3]))

    Plotter.plot_scatter_subplots(3, 1, data_for_plot, subplot_titles)


def run_heatmap_pr_df(dir_path: str, pandemic_rates: np.ndarray, death_factors: np.ndarray, params: Params,
                      pandemic_function: Callable) -> None:
    """
    Runs a given model on different combinations of pandemic rates and colony death factors, thus creating
    a matrix for a heatmap which expresses the fraction of colony birds from the total population.
    :param dir_path: Path to a directory where to save the data
    :param pandemic_rates: Pandemic rate values
    :param death_factors: Colony death factor values
    :param params: The rest of the parameters
    :param pandemic_function: The model pandemic function
    :return: None
    """
    # new_path = mk_dir_for_heatmap(dir_path, model_name=MODEL_NAMES[Model.DETER])

    mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    for i, rate in enumerate(pandemic_rates):
        for j, factor in enumerate(death_factors):

            params.pandemic_rate = rate
            params.c_death_factor = factor

            colony_birds, lone_birds = logistic_growth_model(params, pandemic_function)
            # save_single_run(new_path, params, [colony_birds, lone_birds], MODEL_NAMES[Model.DETER])
            total_last_100 = colony_birds[900:] + lone_birds[900:]
            mat[i][j] = np.average(colony_birds[900:] / total_last_100)

    Plotter.plot_heatmap(mat, death_factors, pandemic_rates, xaxis_title=PARAM_NAMES[ParamName.C_DEATH_FACTOR],
                         yaxis_title=PARAM_NAMES[ParamName.PANDEMIC_RATE], legend_title=FRAC_OF_COLONY_BIRDS_TITLE)
    # mk_heatmap_header(new_path, MODEL_NAMES[Model.DETER], COLONY_BIRDS_STR)
    # save_heatmap_data(new_path, death_factors, pandemic_rates, mat)