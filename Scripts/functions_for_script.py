import numpy as np
from utils.Auxiliary import Params, ParamName, PARAM_NAMES, BirdsPopulations, MODEL_NAMES, Model
from discrete_model.logistic_growth_model import logistic_growth_model
from typing import Tuple, Callable, List
from utils.Plotter import Plotter
from utils.DataSaver import mk_dir_for_heatmap, save_heatmap_data, save_single_run, mk_dir_for_stoch_avg,\
    mk_heatmap_header
FRAC_OF_COLONY_BIRDS_TITLE = "Fraction of colony birds"
FRAC_OF_COLONY_WINS = "Fraction of colony birds wins"
FRAC_OF_LONE_BIRDS_TITLE = "Fraction of lone birds"
FRAC_OF_CO_EX_TITLE = "Fraction of coexistence"
COLONY_WINS, LONE_WINS, COEXISTENCE = "Colony wins", "Lone wins", "Coexistence"
DETER_MODEL = "deterministic_model"
MIN_FRAC_FOR_WIN = 0.95


def run_several_scenarios(dir_path: str, pandemic_function: Callable, subplot_titles: Tuple,
                          params_arr: List[Params], model_name: str) -> None:
    """
    A function that runs a given model in several scenarios, then plots them as subplots.
    :param dir_path: The directory in which to save the data.
    :param pandemic_function: The model pandemic function.
    :param subplot_titles: Titles of the scenarios.
    :param params_arr: An array containing the parameters for the scenarios.
    :param model_name: The name of the model.
    :return: None
    """
    data_for_plot = []

    for params in params_arr:
        colony_birds, lone_birds = logistic_growth_model(params, pandemic_function)
        save_single_run(dir_path, params, BirdsPopulations(colony_birds, lone_birds), model_name)
        data_for_plot.append([colony_birds, lone_birds])

    Plotter.plot_scatter_subplots(len(params_arr), 1, data_for_plot, subplot_titles)


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


def run_stochastic_model_average(num_of_runs: int, pandemic_func: Callable, model_name: str,
                                 params: Params, dir_path: str) -> Tuple[float, float, float]:
    """
    Runs the stochastic model 'num_of_runs' times. At each run calculates the average fraction of colony birds
    in the last 100 generations. Then it checks what scenario has occurred: Colony birds overtook, Lone birds
    overtook, Coexistence. It returns the fraction of each of the scenarios from the total number of runs.
    This function is used to run on a single set of parameters.
    :param num_of_runs - The number of times to perform the stochastic simulation
    :param pandemic_func - The stochastic model function
    :param model_name - The stochastic model name
    :param params - Parameters for the simulation
    :param dir_path - path to a directory where to save the simulation data
    :return A tuple that contains three values: Fraction of wins of the colony birds,
     fraction of wins for the lone birds, fraction of coexistence wins.
    """
    colony_wins, lone_wins, coexist_wins = 0, 0, 0
    # new_dir_path = mk_dir_for_stoch_avg(dir_path, params, model_name)

    for i in range(num_of_runs):
        colony_birds, lone_birds = logistic_growth_model(params, pandemic_func)
        # save_single_run(new_dir_path, params, [colony_birds, lone_birds], model_type=model_name)
        colony_last_100, lone_last_100 = colony_birds[900:], lone_birds[900:]
        total_last_100 = colony_last_100 + lone_last_100
        avg_frac = np.average(colony_last_100 / total_last_100)
        if avg_frac > MIN_FRAC_FOR_WIN:
            colony_wins += 1
        elif avg_frac < (1 - MIN_FRAC_FOR_WIN):
            lone_wins += 1
        else:
            coexist_wins += 1
    return colony_wins / num_of_runs, lone_wins / num_of_runs, coexist_wins / num_of_runs


def run_stoch_heatmaps_pr_df(num_of_runs: int, pandemic_func: Callable, model_name: str, pandemic_rates: np.ndarray,
                             death_factors: np.ndarray, params: Params, dir_path: str) -> None:
    """
    Runs simulations for a heatmap of a stochastic model. The result is a plot with three
    heatmaps showing the average fractions of colony birds, lone birds, coexistence.
    :param num_of_runs: The number of times to run the simulation on each (pandemic rate, colony death factor) pair.
    :param pandemic_func: The stochastic model function
    :param model_name:
    :param pandemic_rates:
    :param death_factors:
    :param params: The rest of the parameters
    :param dir_path: A path to a directory where to save the data
    :return: None
    """

    # new_path = mk_dir_for_heatmap(dir_path, model_name)
    new_path = ""

    colony_win_mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    lone_win_mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    coexist_mat = np.empty(shape=(pandemic_rates.size, death_factors.size))

    for i, rate in enumerate(pandemic_rates):
        for j, factor in enumerate(death_factors):
            params.pandemic_rate = rate
            params.c_death_factor = factor
            colony_win_frac, lone_win_frac, coexist_frac = \
                run_stochastic_model_average(num_of_runs, pandemic_func, model_name, params, new_path)
            colony_win_mat[i][j] = colony_win_frac
            lone_win_mat[i][j] = lone_win_frac
            coexist_mat[i][j] = coexist_frac

    subplot_titles = (FRAC_OF_COLONY_BIRDS_TITLE, FRAC_OF_LONE_BIRDS_TITLE, FRAC_OF_CO_EX_TITLE)
    param_names = [PARAM_NAMES[ParamName.C_DEATH_FACTOR], PARAM_NAMES[ParamName.PANDEMIC_RATE]]
    Plotter.plot_heatmap_subplots(1, 3, [colony_win_mat, lone_win_mat, coexist_mat], [death_factors, pandemic_rates],
                                  subplot_titles, param_names)
    # mk_heatmap_header(new_path, model_name, COLONY_WINS)
    # mk_heatmap_header(new_path, model_name, LONE_WINS)
    # mk_heatmap_header(new_path, model_name, COEXISTENCE)
    # save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, COLONY_WINS)
    # save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, LONE_WINS)
    # save_heatmap_data(new_path, death_factors, pandemic_rates, colony_win_mat, COEXISTENCE)


def run_stoch_single_heatmap(num_of_runs, pandemic_function, model_name, pandemic_rates, death_factors, params, dir_path):
    new_path = mk_dir_for_heatmap(dir_path, model_name)

    colony_win_mat = np.empty(shape=(pandemic_rates.size, death_factors.size))
    for i, rate in enumerate(pandemic_rates):
        for j, factor in enumerate(death_factors):
            params.pandemic_rate = rate
            params.c_death_factor = factor
            colony_win_frac, lone_win_frac, coexist_frac = \
                run_stochastic_model_average(num_of_runs, pandemic_function, model_name, params, new_path)
            colony_win_mat[i][j] = colony_win_frac
    Plotter.plot_heatmap(colony_win_mat, death_factors, pandemic_rates,
                         xaxis_title=PARAM_NAMES[ParamName.C_DEATH_FACTOR],
                         yaxis_title=PARAM_NAMES[ParamName.PANDEMIC_RATE],
                         legend_title=FRAC_OF_COLONY_WINS)


