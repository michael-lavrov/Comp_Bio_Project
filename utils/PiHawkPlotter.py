import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DEFAULT_FONT = 'Calibri'
DEFAULT_FONT_SIZE = 24
STYLE_CONFIG = {'family': DEFAULT_FONT, 'size': DEFAULT_FONT_SIZE}


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
        return go.Figure(data=[go.Scatter(x=generations, y=lone_birds, name="Lone birds"),
                        go.Scatter(x=generations, y=colony_birds, name="Colony birds")],
                        layout={"xaxis": {"title": "Generations"}, "yaxis": {"title": "Number of birds"},
                          "title": f"{model_name}", "font":STYLE_CONFIG})


    @staticmethod
    def plot_average_fraction_of_wins(pandemic_chances, wins_fractions_arr, title):
        """
        Plots the average fraction of gathering birds win as a function of the chance for a pandemic each year.
        :param pandemic_chances: Range of pandemic chances.
        :param wins_fractions_arr: The average fractions array.
        :return: None.
        """
        go.Figure(data=[go.Scatter(x=pandemic_chances, y=wins_fractions_arr)],
                  layout={"xaxis": {"title": "parameter"}, "yaxis": {"title": "Fraction of colony birds"},
                  "title": title}).show()

    @staticmethod
    def plot_heatmap(mat: np.ndarray, stats1: np.ndarray, stats2: np.ndarray,
                     title_text: str = None, xaxis_title: str = None,
                     yaxis_title: str = None, legend_title=None):

        fig = go.Figure(data=[go.Heatmap(x=stats1, y=stats2, z=mat,
                                   colorbar=dict(title=legend_title), colorscale="darkmint")],
          layout={"xaxis": {"title": xaxis_title}, "yaxis": {"title": yaxis_title},
                  "title": title_text})
        fig.update_layout(font=STYLE_CONFIG)
        fig.show()

    @staticmethod
    def plot_scatter_subplots(num_rows, num_cols, data, subplot_titles):
        """
        data: [ [colony_birds, lone_birds], [colony_birds, lone_birds],  ... ]
        """
        font = "Calibri"
        font_size = 20
        fig = make_subplots(rows=num_rows, cols=num_cols, shared_xaxes=False, x_title=None,
                            y_title=None, subplot_titles=subplot_titles)
        fig.update_annotations(font=dict(family=font, size=font_size))
        color1, color2 = "red", "blue"
        for i in range(num_rows):
            for j in range(num_cols):
                colony_birds, lone_birds = data[i+j][0], data[i+j][1]
                generations = np.arange(len(colony_birds))
                if i == j == 0:
                    fig.add_trace(go.Scatter(x=generations, y=colony_birds, marker=dict(color=color1),
                                             name='Colony Birds'), row=i+1, col=j+1)
                    fig.add_trace(go.Scatter(x=generations, y=lone_birds, marker=dict(color=color2),
                                             name='Lone Birds'), row=i+1, col=j+1)
                else:
                    fig.add_trace(
                        go.Scatter(x=generations, y=colony_birds, marker=dict(color=color1),
                                   showlegend=False), row=i + 1, col=j + 1)

                    fig.add_trace(go.Scatter(x=generations, y=lone_birds, marker=dict(color=color2),
                                             showlegend=False), row=i + 1, col=j + 1)
        fig.update_layout(font=dict(family=font, size=font_size-2))
        fig['layout']['xaxis']['title'] = "Generations"
        fig['layout']['yaxis']['title'] = "Birds number"
        fig['layout']['xaxis2']['title'] = "Generations"
        fig['layout']['yaxis2']['title'] = "Birds number"
        fig['layout']['xaxis3']['title'] = "Generations"
        fig['layout']['yaxis3']['title'] = "Birds number"
        fig.show()

    @staticmethod
    def plot_heatmap_subplots(num_rows, num_cols, data, params, subplot_titles, param_names=None):
        """
        params: [ [params0], [params1] ]
        data: [ matrix1, matrix2, ... ]
        param_names: (param0, param1)
        """
        font = "Calibri"
        font_size = 20
        fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=subplot_titles, x_title=param_names[0],
                            y_title=param_names[1])
        fig.update_annotations(font=dict(family=font, size=font_size))

        for i in range(num_rows):
            for j in range(num_cols):
                if i == j == 0:
                    fig.add_trace(go.Heatmap(x=params[0], y=params[1], z=data[i+j], colorscale="darkmint"),
                                  row=i+1, col=j+1)
                else:
                    fig.add_trace(go.Heatmap(x=params[0], y=params[1], z=data[i + j], colorscale="darkmint",
                                             showscale=False), row=i + 1, col=j + 1)

        fig.update_layout(height=500)

        fig.show()

    @staticmethod
    def plot_bar_plot(x_values, y_values, x_title, y_title, plot_title):
        """
        Creates a bar plot with the given values.
        """
        fig = go.Figure(data=[go.Bar(x=x_values, y=y_values)],
                        layout={"xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "title": plot_title})
        fig.show()


