import os
from datetime import datetime
import pandas as pd
import numpy as np


def mk_dir_for_stoch_avg(dir_path, params, model_name):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    new_dir = os.path.join(dir_path, f'{model_name}_{date_time}')
    os.makedirs(new_dir, exist_ok=True)
    header_file_path = os.path.join(new_dir, "avg_runs_header.txt")
    pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations,\
    growth_rate, initial_num_of_birds, carrying_capacity = params

    with open(header_file_path, 'w') as file:
        file.write(f"Average runs for {model_name} at: {date_time}\n\n")
        file.write(f"The fixed parameters are:\nCarrying capacity: {carrying_capacity}\n"
                   f"Initial number of birds: {initial_num_of_birds}\nNumber of generations: {number_of_generations}\n\n")
        file.write(f"The changing parameters are:\nPandemic rate: {pandemic_rate}\n"
                   f"\nSelection coefficient: {selection_coefficient}\nColony birds death factor:{c_death_factor}\n"
                   f"Lone birds death factor: {l_death_factor}\n\n")

    return new_dir


def mk_heatmap_header(dir_path, model_name, heatmap_type):

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


def save_heatmap_data(dir_path, x_axis, y_axis, data, map_name=""):

    data_file_path = os.path.join(dir_path, f'{map_name}_heatmap_data.csv')
    df = pd.DataFrame(data=data, index=y_axis, columns=x_axis)
    df.to_csv(data_file_path)


def save_single_run(dir_path, parameters, birds_populations, model_type=None):

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")

    new_dir = os.path.join(dir_path, f'{model_type}_run_{date_time}')
    os.makedirs(new_dir, exist_ok=True)

    pandemic_rate, selection_coefficient, c_death_factor, l_death_factor, number_of_generations = \
        parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]
    growth_rate, initial_num_of_birds, carrying_capacity = parameters[5], parameters[6], parameters[7]

    header_file_path = os.path.join(new_dir, f'{model_type}_run_{date_time}.txt')
    with open(header_file_path, 'w') as file:
        file.write(f"{model_type} model run at {date_time}\n\n")
        file.write(f"The fixed parameters are:\nCarrying capacity: {carrying_capacity}\n"
                   f"Initial number of birds: {initial_num_of_birds}\nNumber of generations: {number_of_generations}\n\n")
        file.write(f"The changing parameters are:\nPandemic rate: {pandemic_rate}\n"
                   f"\nSelection coefficient: {selection_coefficient}\nColony birds death factor:{c_death_factor}\n"
                   f"Lone birds death factor: {l_death_factor}\n\n")

        file.write("Total population, Colony birds population, Lone birds population, Colony birds fraction")

    data_file_path = os.path.join(new_dir, f'{model_type}_run_data_{date_time}.csv')

    colony_birds, lone_birds = birds_populations[0], birds_populations[1]
    total_birds = colony_birds + lone_birds
    colony_birds_frac = colony_birds / total_birds
    generations = [i for i in range(1, 1001)]

    columns = ["Total population", "Colony birds population", "Lone birds population", "Colony birds fraction"]
    data = np.column_stack((total_birds, colony_birds, lone_birds, colony_birds_frac))
    df = pd.DataFrame(data=data, index=generations, columns=columns)
    df.to_csv(data_file_path)








