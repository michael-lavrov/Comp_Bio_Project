import sys
from discrete_model.pandemic_functions import types_shift_model_deter_function, deterministic_pandemic_function
from differential_model.logistic_growth_diff import logistic_growth_diff
from discrete_model.logistic_growth_model import logistic_growth_model
from utils.DataSaver import save_single_run, make_new_dir
from utils.Plotter import Plotter
from utils.Auxiliary import Params, BirdsPopulations, MODEL_NAMES, Model
# Constant values of unchanging parameters
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
GROWTH_RATE = 1.5
NUM_OF_GENERATIONS = 1000
# Pandemic rates for the three single run scenarios.
RATE1, RATE2, RATE3 = 0.05, 0.1, 1/14
SHIFT_FACTOR = 0.01

C_WIN_PARAMS = Params(pandemic_rate=RATE1, selection_coefficient=0.05, c_death_factor=0.5, shift_factor=SHIFT_FACTOR,
                      l_death_factor=0, num_of_generations=NUM_OF_GENERATIONS, growth_rate=GROWTH_RATE,
                      init_birds_num=INITIAL_NUM_OF_BIRDS, carrying_capacity=CARRYING_CAPACITY)
L_WIN_PARAMS = C_WIN_PARAMS.copy()
L_WIN_PARAMS.pandemic_rate = RATE2
CO_EX_PARAMS = C_WIN_PARAMS.copy()
CO_EX_PARAMS.pandemic_rate = RATE3

TYPE_SHIFT = "TypeShift"

# Parameters order for types shift: pandemic_rate, selection_coefficient, c_pandemic_death_rate, strategy_change_factor,
# l_pandemic_death_rate, num_of_generations, growth_rate, init_num_of_birds, carrying_capacity

def run_single_types_shift_dynamics(dir_path):

    params1 = Params(pandemic_rate=0.1, selection_coefficient=0.1, c_death_factor=0.5, l_death_factor=0.5,
                    growth_rate=0.1, carrying_capacity=10000, init_birds_num=3000, shift_factor=0.01,
                    num_of_generations=1000)
    params2 = params1.copy()
    params2.c_death_factor = 0.7
    params3 = params1.copy()
    params3.c_death_factor = 0.8
    params4 = params1.copy()
    params4.c_death_factor = 0.95

    new_path = make_new_dir(dir_path, "types_shift_comparison")

    populations1 = BirdsPopulations(*logistic_growth_model(params1, types_shift_model_deter_function))
    save_single_run(new_path, params1, populations1, MODEL_NAMES[Model.TYPE_SHIFT])

    populations2 = BirdsPopulations(*logistic_growth_model(params2, types_shift_model_deter_function))
    save_single_run(new_path, params2, populations2, MODEL_NAMES[Model.TYPE_SHIFT])

    populations3 = BirdsPopulations(*logistic_growth_model(params3, types_shift_model_deter_function))
    save_single_run(new_path, params3, populations3, MODEL_NAMES[Model.TYPE_SHIFT])

    populations4 = BirdsPopulations(*logistic_growth_model(params4, types_shift_model_deter_function))
    save_single_run(new_path, params4, populations4, MODEL_NAMES[Model.TYPE_SHIFT])

    subplot_titles = (f"colony death factor: {params1.c_death_factor}", f"colony death factor: {params2.c_death_factor}",
                      f"colony death factor: {params3.c_death_factor}", f"colony death factor: {params4.c_death_factor}")

    Plotter.plot_scatter_subplots(4, 1, [populations1, populations2, populations3, populations4], subplot_titles)


def run_single_example(dir_path: str, params: Params):

    # new_path = make_new_dir(dir_path, "type_shift_single_run")

    colony_birds, lone_birds = logistic_growth_diff(params, types_shift_model_deter_function)
    bird_populations = BirdsPopulations(colony_birds, lone_birds)
    # save_single_run(new_path, params, bird_populations, MODEL_NAMES[Model.TYPE_SHIFT])
    Plotter.plot_birds_numbers_scatter_plot(bird_populations.colony_birds, bird_populations.lone_birds,
                                            f"shift factor: {params.shift_factor}").show()


def main():
    # run_single_types_shift_dynamics(sys.argv[1])
    params = Params(pandemic_rate=0.1, selection_coefficient=0.1, c_death_factor=0.8, l_death_factor=0.5,
                    growth_rate=0.1, carrying_capacity=10000, init_birds_num=3000, shift_factor=0.01,
                    num_of_generations=1000)
    run_single_example(sys.argv[1], params)

if __name__ == "__main__":
    main()
