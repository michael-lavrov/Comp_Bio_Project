import numpy as np
import plotly.graph_objects as go


class Plotter:
    """
    A Plotter object that creates different plots by using static methods.
    """
    @staticmethod
    def plot_birds_numbers_scatter_plot(colony_birds, lone_birds, model_name):
        """
        Plots the number of birds of each type as a function of generations of the simulation.
        :param model_name: The models' name to enter the plot title.
        :param colony_birds: The numbers of colony birds in each generation.
        :param lone_birds: The numbers of lone birds in each generation.
        :return: None.
        """
        generations = np.arange(len(colony_birds))
        go.Figure(data=[go.Scatter(x=generations, y=colony_birds, name="Colony birds"),
                        go.Scatter(x=generations, y=lone_birds, name="Lone birds")],
                  layout={"xaxis": {"title": "Years"}, "yaxis": {"title": "Number of birds"},
                          "title": f"{model_name}"}).show()

    @staticmethod
    def plot_average_fraction_of_wins(pandemic_chances, wins_fractions_arr, title):
        """
        Plots the average fraction of gathering birds win as a function of the chance for a pandemic each year.
        :param pandemic_chances: Range of pandemic chances.
        :param wins_fractions_arr: The average fractions array.
        :return: None.
        """
        go.Figure(data=[go.Scatter(x=pandemic_chances, y=wins_fractions_arr)],
                  layout={"xaxis": {"title": "pandemic rate"}, "yaxis": {"title": "Fraction of colony birds"},
                  "title": title}).show()

    @staticmethod
    def plot_heatmap_selection_coeff_pandemic_chance(mat: np.ndarray, chances: np.ndarray, selection_coeffs: np.ndarray,
                                                     title_text: str):

        go.Figure(data=[go.Heatmap(x=chances, y=selection_coeffs, z=mat)],
                  layout={"xaxis": {"title": "pandemic rate"}, "yaxis": {"title": "selection coefficient"},
                          "title": title_text}).show()

