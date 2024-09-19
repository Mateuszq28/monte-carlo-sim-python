import os
import re
import json

t1 = { # example
    "sim_c_filename": "mc456_mc.c",
    "params_type": "original_params",
    "n_photons": 10_000,

    "out_log_default_name": "mc456_log.txt",
    "out_cube_default_name": "mc456_mc_cube.json",
    "out_log_change_name": "mc456_log_10k_original_params.txt",
    "out_cube_change_name": "mc456_mc_10k_original_params_cube.json",

    "script_dir": "original_params",
    "time_wrapper_Dir_id": 1,
    "time_wrapper_Sim_id": 3
}

num_decoder = {
    10_000: "10k",
    100_000: "100k",
    1_000_000: "1mln",
    10_000_000: "10mln",
    100_000_000: "100mln",
    1_000_000_000: "1mld",
    10_000_000_000: "10mld",
    100_000_000_000: "100mld",
}


def make_test_dict(sim_c_filename, params_type, n_photon):
    out_log_default_name = sim_c_filename[:-4] + "log.txt"
    num = num_decoder[n_photon]
    out_log_change_name = sim_c_filename[:-4] + "log" + "_" + num + "_" + params_type + ".txt"

    if sim_c_filename == "mc456_mc.c":
        out_cube_default_name = sim_c_filename[:-2] + "_cube.json"
        out_cube_change_name = sim_c_filename[:-2] + "_" + num + "_" + params_type + "_cube.json"
    else:
        out_cube_default_name = None
        out_cube_change_name = None

    script_dir = "benchmark_sims" if params_type == "my_params" else params_type

    time_wrapper_Sim_id = ["tiny", "small", "mc321", "mc456"].index(sim_c_filename[:-5])
    time_wrapper_Dir_id = ["benchmark_sims", "original_params"].index(script_dir)

    d = {
        "sim_c_filename": sim_c_filename,
        "params_type": params_type,
        "n_photons": n_photon,

        "out_log_default_name": out_log_default_name,
        "out_cube_default_name": out_cube_default_name,
        "out_log_change_name": out_log_change_name,
        "out_cube_change_name": out_cube_change_name,

        # --- from time wrapper: ---
        # sim_names_list = ["tiny", "small", "mc321", "mc456"]
        # sim_name = sim_names_list[3]
        # dirs = ["benchmark_sims", "original_params"]
        # rel_scritpt_dir = dirs[1]

        "script_dir": script_dir,
        "time_wrapper_Dir_id": time_wrapper_Dir_id,
        "time_wrapper_Sim_id": time_wrapper_Sim_id
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



def test_log(data_dict, filename):
    with open(filename, 'w') as f:
        json.dump(data_dict, f)



def run():
    sim_c_filenames = ["mc456_mc.c", "tiny_mc.c", "small_mc.c"]
    params_types = ["original_params", "my_params"]
    n_photons = [10**n for n in range(4,9)]

    # small test
    # sim_c_filenames = ["tiny_mc.c"]
    # params_types = ["original_params"]
    # n_photons = [10_000]


    for n_photon in n_photons:
        for sim_c_filename in sim_c_filenames:
            for params_type in params_types:

                print("iter start")
                # setup dict that describes all features of the test
                print("make_test_dict")
                test_dict = make_test_dict(sim_c_filename, params_type, n_photon)
                print()
                print("===============================================")
                print(test_dict['n_photons'])
                print(test_dict)
                # path to dir with script
                print()
                print("set paths")
                self_path = os.path.dirname(os.path.abspath(__file__))
                script_dir = os.path.join(self_path, test_dict['script_dir'])
                # change nphotons in c source code
                print("edit n photons in c source code")
                cfile_path = os.path.join(script_dir, sim_c_filename)
                exefile_path = os.path.join(script_dir, sim_c_filename[:-1] + "exe")
                objfile_path = os.path.join(script_dir, sim_c_filename[:-1] + "obj")
                if sim_c_filename == "tiny_mc.c":
                    regex_pattern = r".*ID_EDIT_1_1.*"
                    new_sentence = f"long   i, shell, photons = {n_photon}; /*ID_EDIT_1_1*/"
                elif sim_c_filename == "small_mc.c":
                    regex_pattern = r".*ID_EDIT_1_2.*"
                    new_sentence = f"long   i, photons = {n_photon}; /*ID_EDIT_1_2*/"
                elif sim_c_filename == "mc456_mc.c":
                    regex_pattern = r".*ID_EDIT_1_3.*"
                    new_sentence = f"Nphotons    = {n_photon}; /* set number of photons in simulation */ /*ID_EDIT_1_3*/"
                else:
                    print("break!")
                    print(test_dict)
                    break
                replace_line_in_file(cfile_path, regex_pattern, new_sentence)
                # compile
                print("compile")
                print()
                # /Fe - flag to tell where put .exe output file
                # /Fo - flag to tell where put .obj output file
                # /O2 - maximum optimization for speed
                os.system(f"cl {cfile_path} /Fe{exefile_path} /Fo{objfile_path} /O2")
                print()
                # change source code in time wrapper
                print("change time_wrapper.py")
                pywrap_path = os.path.join(self_path, "time_wrapper.py")
                regex_pattern1 = r".*ID_EDIT_2.*"
                regex_pattern2 = r".*ID_EDIT_3.*"
                new_sentence1 = f"sim_name = sim_names_list[{ test_dict['time_wrapper_Sim_id'] }] # ID_EDIT_2"
                new_sentence2 = f"rel_scritpt_dir = dirs[{ test_dict['time_wrapper_Dir_id'] }] # ID_EDIT_3"
                replace_line_in_file(pywrap_path, regex_pattern1, new_sentence1)
                replace_line_in_file(pywrap_path, regex_pattern2, new_sentence2)
                # run using time wrapper
                print("run in time wrapper")
                os.system(f"python {pywrap_path}")
                # rename
                print("rename")
                # rename cube.json
                old_name = test_dict["out_cube_default_name"]
                new_name = test_dict["out_cube_change_name"]
                if old_name is not None:
                    old_name = os.path.join(script_dir, old_name)
                    new_name = os.path.join(script_dir, new_name)
                    os.replace(old_name, new_name)
                # rename log.txt
                old_name = test_dict["out_log_default_name"]
                old_name = os.path.join(script_dir, old_name)
                new_name = test_dict["out_log_change_name"]
                new_name = os.path.join(script_dir, new_name)
                os.replace(old_name, new_name)
                # save state log
                print("log")
                test_log(test_dict, "test_wrapper_log.txt")
                print("iter done")
                


if __name__ == '__main__':
    run()