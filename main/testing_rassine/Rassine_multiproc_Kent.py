#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Rudimentary script to multiprocess Rassine on a list of spectra

Created on Thu Feb  7 16:34:29 2019
Author: Kent Barbey'''

import os
import time
import fileinput
import shutil
import subprocess
import glob
import multiprocessing as mp

# =============================================================================
#  ENTRIES
# =============================================================================

def create_copy(source_path, destination_path):
    shutil.copyfile(source_path, destination_path)

def modify_and_run(file_path,line_number,new_content):
    # Read the content of the file
    with fileinput.FileInput(file_path, inplace=True, backup=".bak") as file:
        for i, line in enumerate(file, start=1):
            # Modify the specified line
            if i == line_number:
                print(new_content)
            else:
                print(line, end="")

    # Run Rassine
    subprocess.run(["python", r"C:\Users\kentb\Desktop\PDM\thesis\main\testing_rassine\Rassine.py"],check=False)
    print("Done")

def run_loop(paths):
    for file_path in paths:
        file_path = file_path.replace("\\","/")
        file_path = file_path.split("/")[-1]
        file_path = '/'+file_path
        print(file_path)
        modify_and_run(r"C:\Users\kentb\Desktop\PDM\thesis\main\testing_rassine\Rassine_config.py", 28, 'spectrum_name = cwd+"/delCep_csv" + "%s"' % file_path)

if __name__ == '__main__':
    # Get the list of spectra
    start_time = time.time()
    cwd = os.getcwd()
    spectrum_names = glob.glob(cwd + "/delCep_csv/*.csv")
    #divide the list of spectra in 4
    spectrum_names1 = spectrum_names[:int(len(spectrum_names)/4)]
    spectrum_names2 = spectrum_names[int(len(spectrum_names)/4):int(len(spectrum_names)/2)]
    spectrum_names3 = spectrum_names[int(len(spectrum_names)/2):int(3*len(spectrum_names)/4)]
    spectrum_names4 = spectrum_names[int(3*len(spectrum_names)/4):]

    # Save the config and the Rassine files
    config_template_path = r"C:\Users\kentb\Desktop\PDM\thesis\main\testing_rassine\Rassine_config.py"
    rassine_template_path = r"C:\Users\kentb\Desktop\PDM\thesis\main\testing_rassine\Rassine.py"

    p1 = mp.Process(target=run_loop, args=(spectrum_names1,))
    p2 = mp.Process(target=run_loop, args=(spectrum_names2,))
    p3 = mp.Process(target=run_loop, args=(spectrum_names3,))
    p4 = mp.Process(target=run_loop, args=(spectrum_names4,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    end_time = time.time()
    print("Total time: " + str(end_time - start_time))
    