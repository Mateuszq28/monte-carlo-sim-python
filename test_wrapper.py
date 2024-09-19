import os
import re
import json
import time
import shutil
from datetime import datetime


num_decoder = {
    0: "0",
    1: "1",
    10: "10",
    100: "100",
    1_000: "1k",
    10_000: "10k",
    100_000: "100k",
    1_000_000: "1mln",
    10_000_000: "10mln",
    100_000_000: "100mln",
    1_000_000_000: "1mld",
    10_000_000_000: "10mld",
    100_000_000_000: "100mld",
}


def make_test_dict(params_type, n_photon):
    num = num_decoder[n_photon]
    experiments_done_subfolder = "t_" + num + "_" + params_type

    d = {
        "params_type": params_type,
        "n_photons": n_photon,
        "experiments_done_subfolder": experiments_done_subfolder
    }

    return d


# Function to find and replace a line in a file based on a regex pattern
def replace_line_in_file(file_path, regex_pattern, new_sentence):
    # Open the file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Open the file in write mode to replace the content
    with open(file_path, 'w') as file:
        for line in lines:
            # If the line matches the regex pattern, replace it with the new sentence
            if re.search(regex_pattern, line):
                file.write(new_sentence + '\n')
            else:
                file.write(line)


def test_log(data_dict, filename, iter_start_time, all_runs_start_time):
    datetime_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time = time.time()
    iter_time = str(end_time - iter_start_time) + " seconds"
    all_runs_time_time = str(end_time - all_runs_start_time) + " seconds"
    # add to log file
    data_dict['datetime_log'] = datetime_log
    data_dict['iter_time'] = iter_time
    data_dict['all_runs_time_time'] = all_runs_time_time
    # print
    print('datetime_log', datetime_log)
    print('iter_time', iter_time)
    print('all_runs_time_time', all_runs_time_time)
    with open(filename, 'w') as f:
        json.dump(data_dict, f)


def copy_folder(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)  # Tworzenie folderu docelowego, jeśli nie istnieje

    # Przechodzimy przez wszystkie pliki i foldery w folderze źródłowym
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(destination_folder, item)

        if os.path.isdir(source_path):
            # Rekursywnie kopiujemy foldery
            copy_folder(source_path, destination_path)
        else:
            # Kopiujemy pliki, zastępując istniejące
            shutil.copy2(source_path, destination_path)



def run():
    params_types = ["my_params", "original_params"]
    n_photons = [10**n for n in range(4,9)]

    all_runs_start_time = time.time()
    for params_type in params_types:
        for n_photon in n_photons:
            print("iter start")
            iter_start_time = time.time()
            # setup dict that describes all features of the test
            print("make_test_dict")
            test_dict = make_test_dict(params_type, n_photon)
            print()
            print("===============================================")
            print(test_dict['n_photons'])
            print(num_decoder[ test_dict['n_photons'] ] + " photons")
            print(test_dict)
            # path to dir with script
            print()
            print("set paths")
            self_dir = os.path.dirname(os.path.abspath(__file__))
            # change nphotons
            print("edit n photons in source code")
            make_light_script = os.path.join(self_dir, "Make.py")
            regex_pattern = r".*ID_EDIT_1.*"
            new_sentence = f"        lightSource.initialize_source(photon_limit={n_photon}) # ID_EDIT_1"
            replace_line_in_file(make_light_script, regex_pattern, new_sentence)
            # setup config file - copy and overwrite old one
            print("setup config file - copy and overwrite old one")
            config_file = "config_" + params_type + ".json"
            source_path = os.path.join(self_dir, config_file)
            destination_path = os.path.join(self_dir, "config.json")
            shutil.copy2(source_path, destination_path)
            # run
            print("run sim")
            os.system("python Sim.py")
            # move files to subfolder
            print("move result and setup files to subfolder")
            main_out_dir = os.path.join(self_dir, "experiments_done", test_dict["experiments_done_subfolder"])
                # envs/*
            source_folder = os.path.join(self_dir, "envs")
            destination_folder = os.path.join(main_out_dir, "envs")
            copy_folder(source_folder, destination_folder)
                # config.json
            source_path = os.path.join(self_dir, "config.json")
            destination_path = os.path.join(main_out_dir, "config.json")
            shutil.copy2(source_path, destination_path)
                # lightSources/*
            source_folder = os.path.join(self_dir, "lightSources")
            destination_folder = os.path.join(main_out_dir, "lightSources")
            copy_folder(source_folder, destination_folder)
                # propSetups/*
            source_folder = os.path.join(self_dir, "propSetups")
            destination_folder = os.path.join(main_out_dir, "propSetups")
            copy_folder(source_folder, destination_folder)
                # resultRecords/*
            source_folder = os.path.join(self_dir, "resultRecords")
            destination_folder = os.path.join(main_out_dir, "resultRecords")
            copy_folder(source_folder, destination_folder)
            # save state log
            print("log")
            test_log(test_dict, "test_wrapper_log.txt", iter_start_time, all_runs_start_time)
            print("iter done")
                


if __name__ == '__main__':
    run()
