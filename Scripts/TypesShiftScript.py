import sys
from discrete_model.TypesShiftModel import types_shift_model
from discrete_model.DetermenisticModel import logistic_growth_model
from utils.DataSaver import save_single_run, make_new_dir
from utils.PiHawkPlotter import Plotter
# Constant values of unchanging parameters
INITIAL_NUM_OF_BIRDS = 3000
CARRYING_CAPACITY = 10000
GROWTH_RATE = 1.5
NUM_OF_GENERATIONS = 1000
# Pandemic rates for the three single run scenarios.
RATE1, RATE2, RATE3 = 0.05, 0.1, 1/14
SHIFT_FACTOR = 0.01


C_WIN_PARAMS = [RATE1, 0.05, 0.5, SHIFT_FACTOR, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
L_WIN_PARAMS = [RATE2, 0.05, 0.5, SHIFT_FACTOR, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
CO_EX_PARAMS = [RATE3, 0.05, 0.5, SHIFT_FACTOR, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
TYPE_SHIFT = "TypeShift"

# Parameters order for types shift: pandemic_rate, selection_coefficient, c_pandemic_death_rate, strategy_change_factor,
# l_pandemic_death_rate, num_of_generations, growth_rate, init_num_of_birds, carrying_capacity

def run_single_types_shift_dynamics(dir_path):

    new_path = make_new_dir(dir_path, "types_shift_single_dynamics")
    data_for_plot = []
    # Colony birds winning scenario:
    colony_birds_1, lone_birds_1 = types_shift_model(*C_WIN_PARAMS)
    save_single_run(new_path, C_WIN_PARAMS, [colony_birds_1, lone_birds_1], TYPE_SHIFT)
    data_for_plot.append(([colony_birds_1, lone_birds_1]))
    # Lone birds winning scenario
    colony_birds_2, lone_birds_2 = types_shift_model(*L_WIN_PARAMS)
    save_single_run(new_path, L_WIN_PARAMS, [colony_birds_2, lone_birds_2], TYPE_SHIFT)
    data_for_plot.append(([colony_birds_2, lone_birds_2]))
    # Coexistence scenario
    colony_birds_3, lone_birds_3 = types_shift_model(*CO_EX_PARAMS)
    save_single_run(new_path, CO_EX_PARAMS, [colony_birds_3, lone_birds_3], TYPE_SHIFT)
    data_for_plot.append(([colony_birds_3, lone_birds_3]))

    subplot_titles = (f'Pandemic rate: {RATE1}', f'Pandemic rate: {RATE2}', f'Pandemic rate: {round(RATE3, 3)}')

    Plotter.plot_scatter_subplots(3, 1, data_for_plot, subplot_titles)


def run_single_example(dir_path):

    new_path = make_new_dir(dir_path, "types_shift_comparison")
    data_for_plot = []
    params = [1/14, 0.05, 0.5, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS, CARRYING_CAPACITY]
    params_ts = [1/14, 0.05, 0.5, SHIFT_FACTOR, 0, NUM_OF_GENERATIONS, GROWTH_RATE, INITIAL_NUM_OF_BIRDS,
                 CARRYING_CAPACITY]

    colony_birds, lone_birds = logistic_growth_model(*params)
    data_for_plot.append([colony_birds, lone_birds])
    save_single_run(new_path, params, [colony_birds, lone_birds], TYPE_SHIFT)

    colony_birds_ts, lone_birds_ts = types_shift_model(*params_ts)
    data_for_plot.append([colony_birds_ts, lone_birds_ts])
    save_single_run(new_path, params_ts, [colony_birds_ts, lone_birds_ts], TYPE_SHIFT)

    subplot_titles = (f'Deterministic', f'Type switch')

    Plotter.plot_scatter_subplots(2, 1, data_for_plot, subplot_titles)


def main():
    # run_single_types_shift_dynamics(sys.argv[1])
    run_single_example(sys.argv[1])

if __name__ == "__main__":
    main()