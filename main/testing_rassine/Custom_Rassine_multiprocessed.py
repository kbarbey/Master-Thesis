#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Rudimentary script to multiprocess Rassine on a list of spectra

Created on 16.12.2023
Author: Kent Barbey'''
import sys
sys.path.append(r"C:\Users\kentb\Desktop\PDM\thesis\main\testing_rassine")
import os
import time
import math
import fileinput
import shutil
import subprocess
import glob
import multiprocessing as mp
import Rassine
from Rassine_config import config


def run_loop(spectrum_names):
    '''Runs Rassine on a list of spectra'''
    config1 = config.copy()
    for spectrum_name in spectrum_names:
        config1['spectrum_name'] = spectrum_name
        Rassine.rassine(config1)
    print('Done')

if __name__ == '__main__':
    # Get the list of spectra
    start_time = time.time()
    cwd = os.getcwd()
    spectrum_names = glob.glob(cwd + "/barnard_missing/*.csv")
    l = len(spectrum_names)
    print("Number of spectra: " + str(len(spectrum_names)), flush=True)
    #number of cores
    num_cores = mp.cpu_count()-7
    spec_per_core = math.ceil(l/num_cores)
    print("Number of cores: " + str(num_cores), flush=True)
    print("Number of spectra per core: " + str(spec_per_core), flush=True)
    #divide the list of spectra in num_cores parts
    processes = []
    divided_spectrum_names = []
    for i in range(num_cores):
        if i == num_cores-1:
            specs = spectrum_names[spec_per_core*i:]
        else:
            specs = spectrum_names[spec_per_core*i:spec_per_core*(i+1)]
        divided_spectrum_names.append(specs)
    for idx, specs in enumerate(divided_spectrum_names):
        print("Number of spectra in process " + str(idx+1) + ": " + str(len(specs)), flush=True)
        p = mp.Process(target=run_loop, args=(specs,))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    end_time = time.time()
    print("Total time: " + str(end_time - start_time), flush=True)

    