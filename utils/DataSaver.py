import os
from datetime import datetime
import pandas as pd
import numpy as np
from utils.Auxiliary import Params, BirdsPopulations


def mk_dir_for_stoch_avg(dir_path: str, params: Params, model_name: str):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    new_dir = os.path.join(dir_path, f'{model_name}_{date_time}')
    os.makedirs(new_dir, exist_ok=True)
    header_file_path = os.path.join(new_dir, "avg_runs_header.txt")
    params.write_to_file(header_file_path)

    return new_dir


def make_header_file(dir_path: str, model_name: str, date_time: str, params: Params) -> None:
    """
    Creates a header file for a simulation and writes the parameters that were used in the simulation.
    :param dir_path: Path to directory in which to save the file.
    :param model_name: The name of the model that was used.
    :param date_time: Date and time of the simulation.
    :param params: Parameters that were used in the simulation.
    """
    header_file_path = os.path.join(dir_path, f"{model_name}_run_header.txt")
    with open(header_file_path, 'a') as file:
        file.write(f"Simulation run for {model_name} at: {date_time}\n\n")
    params.write_to_file(header_file_path)


def mk_heatmap_header(dir_path: str, model_name: str, heatmap_type: str):

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    header_file_path = os.path.join(dir_path, f"{heatmap_type}_heatmap_header.txt")
    with open(header_file_path, 'w') as file:
        file.write(f"{heatmap_type} heatmap run at {date_time}\n\n")
        file.write(f"Model: {model_name}\n")
        file.write("x_axis: Death factor\n")
        file.write("y_axis: Pandemic rate\n")
        file.write(f"Color: Fraction of {heatmap_type}")


def mk_dir_for_heatmap(dir_path, model_name=""):

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    new_dir = os.path.join(dir_path, f'{model_name}_{date_time}')
    os.makedirs(new_dir, exist_ok=True)

    return new_dir


def make_new_dir(dir_path, dir_name):

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    new_dir = os.path.join(dir_path, f'{dir_name}_{date_time}')
    os.makedirs(new_dir, exist_ok=True)

    return new_dir


def save_heatmap_data(dir_path, x_axis, y_axis, data, map_name=""):

    data_file_path = os.path.join(dir_path, f'{map_name}_heatmap_data.csv')
    df = pd.DataFrame(data=data, index=y_axis, columns=x_axis)
    df.to_csv(data_file_path)


def save_single_run(dir_path: str, params: Params, birds_populations: BirdsPopulations, model_name: str):

    # Creating new directory for the run
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    new_dir_path = os.path.join(dir_path, f'{model_name}_run_{date_time}')
    os.makedirs(new_dir_path, exist_ok=True)
    # Creating header file
    make_header_file(new_dir_path, model_name, date_time, params)
    # Creating data file and saving data
    data_file_path = os.path.join(new_dir_path, f'{model_name}_run_data_{date_time}.csv')
    generations = [i for i in range(1, params.num_of_generations+1)]
    columns = ["Total population", "Colony birds population", "Lone birds population", "Colony birds fraction"]
    data = np.column_stack((birds_populations.get_total_birds_num(), birds_populations.colony_birds,
                            birds_populations.lone_birds, birds_populations.get_frac_of_colony_birds()))
    df = pd.DataFrame(data=data, index=generations, columns=columns)
    df.to_csv(data_file_path)


def data_extractor(path):

    df = pd.read_csv(path)
    data = df.iloc[:, 1:].to_numpy()
    death_factors = df.columns.to_numpy()[1:]
    pandemic_rates = df.iloc[:, 0].to_numpy()
    return data, death_factors, pandemic_rates












