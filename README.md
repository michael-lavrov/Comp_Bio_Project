Seabird Population Dynamics Simulator
Overview
The Seabird Population Dynamics Simulator is a research project in computational biology aimed at studying the impact of epidemics on seabird populations, focusing on their lifestyle (colony or solitary).
This project utilizes simulations based on logistic growth equations to analyze and understand the dynamics of seabird populations under various conditions.

Technology Stack
The project is implemented in Python and makes use of the following libraries:

numpy
plotly
sys
pandas
dataclass
os
Target Audience
This project is primarily designed for recruiters seeking developers with expertise in computational biology, data analysis, and simulation modeling.

Purpose
The Seabird Population Dynamics Simulator provides an environment for running simulations with different sets of parameters.
It offers functionality to save simulation data and generate plots to visualize the results.

Key Components
The discrete_model directory includes two crucial files:

logistic_growth_model.py: This file serves as the core of the simulation, implementing the logistic growth model.
It receives a callable argument, known as a "pandemic function", enabling flexibility in modeling various scenarios.

pandemic_functions.py: This file contains different functions that simulate variations of pandemic scenarios.
These functions can be used as arguments for the logistic growth model, allowing for the exploration of different pandemic dynamics within the simulation environment.

Integration of the logistic model with pandemic functions provides versatility in analyzing the impact of epidemics on seabird populations under different conditions.

utils Directory
The utils directory contains essential components for the simulator:

Auxilliary.py: This file contains classes that facilitate the manipulation of model variables within the simulation environment.
DataSaver.py: Functions in this file are responsible for saving data generated during simulations.
Plotter.py: This file houses a class with static methods used to create charts for presenting simulation results.

Future Development
Future development of this project will focus on running the model with different parameters to further study the dynamics of seabird populations under varying conditions.
