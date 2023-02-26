import random
import numpy as np
from datetime import datetime
import pickle
DATA_DIR_PATH = "data"


class DataManager:
    """
    An object that stores data for a single simulation,
    """
    def __init__(self, pandemic_prob: float, selection_coefficient: float, pandemic_death_coeff: float):
        self.date_time = datetime.now()
        self.seed_arr = []
        self.pandemic_prob = pandemic_prob
        self.selection_coefficient = selection_coefficient
        self.pandemic_death_coeff = pandemic_death_coeff

    def generate_seed(self):
        """
        Chooses seed for random variables.
        :return: None
        """
        seed = random.randint(0, 1000000)
        self.seed_arr.append(seed)
        random.seed(seed)
        np.random.seed(seed)

    def get_datetime_str(self):
        return self.date_time

    def get_seeds(self):
        return self.seed_arr

    def get_pandemic_prob(self) -> float:
        return self.pandemic_prob

    def get_selection_coefficient(self) -> float:
        return self.selection_coefficient

    def get_pandemic_death_coeff(self) -> float:
        return self.pandemic_death_coeff

    @staticmethod
    def save_data_manager_obj(data_manager):
        """
        Saves a DataManager object into a 'pickle' file.
        :param data_manager: SeedSaver object
        :return: None.
        """
        date_time = data_manager.get_datetime_str()
        date_time = date_time.strftime('%d-%m-%Y_%H-%M')
        file_path = f"{DATA_DIR_PATH}/{date_time}.pickle"
        with open(file_path, 'wb') as file:
            pickle.dump(data_manager, file)

    @staticmethod
    def retrieve_data_manager_obj(path):
        """
        Retrieves a DataManager object.
        :param path: Path to the 'pickle' file.
        :return: SeedSaver object.
        """
        with open(path, 'rb') as file:
            date_manager = pickle.load(file)

        return date_manager



