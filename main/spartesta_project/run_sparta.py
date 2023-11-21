import os
import csv
from sparta.Auxil.PeriodicityDetector import PeriodicityDetector
from sparta.UNICOR.Spectrum import Spectrum
from sparta.UNICOR.Template import Template
from sparta.Auxil.TimeSeries import TimeSeries
from sparta.Observations import Observations
import numpy as np
import pandas as pd

# Specify the parent directory containing all the folders
# spectra_directory = "/home/astro/kbarbey/pdm/data/HERMES/SPECTRA/"
# rv_directory = "/home/astro/kbarbey/pdm/data/HERMES/RV/"

# List all subdirectories (folders) in the parent directory
# spectra_folders = sorted([os.path.join(spectra_directory,folder) for folder in os.listdir(spectra_directory) if os.path.isdir(os.path.join(spectra_directory, folder))])
# rv_folders = sorted([os.path.join(rv_directory,folder) for folder in os.listdir(rv_directory)])
#print(spectra_folders,rv_folders)

list_wv =[[4450,4400,4350,4300,4250,4200,4150,4100,4050,4000],[4550,4600,4650,4700,4750,4800,4850,4900,4950,5000]] 

# Loop over all subdirectories
#for rv_folder, spectra_folder in zip(rv_folders, spectra_folders):
for min_wv, max_wv in zip(list_wv[0],list_wv[1]):

    # DATA PARAMETERS

    survey = "HERMES" # survey name
    sample_rate = 1 # sample rate of the data
    #min_wv = 4000 # minimum wavelength of the data
    #max_wv = 6000 # maximum wavelength of the data
    spec_dir = "/home/astro/kbarbey/pdm/data/HERMES/SPECTRA/RRLyr_Hermes_spectra"#spectra_folder  # directory of the spectra
    rv_dir = "/home/astro/kbarbey/pdm/data/HERMES/RV/RRLyr_Hermes.csv" #rv_folder  # directory of the RVs

    # LOAD DATA

    obs_data = Observations(survey=survey, sample_rate=sample_rate, min_wv=min_wv, max_wv=max_wv,
                            target_visits_lib=spec_dir)
    df = pd.read_csv(rv_dir)
    rv = df.rv.astype(float).values
    e_rv = df.rv_err.astype(float).values
    times = df.bjd.astype(float).values
    if survey == "CORALIE": 
        ids = df.unique_id.astype(str).values
    elif survey == "HERMES":
        ids = df.unique_id.astype(int).values

    # PERIODOGRAM PARAMETERS

    baseline = int(abs(obs_data.time_series.times[-1]-obs_data.time_series.times[0]))
    min_freq = 1/2/baseline # Or maybe 1/2/baseline to be sure but let's test it that way.
    max_freq = 2 # depends on the star.
    freq_range = (min_freq, max_freq) # frequency range of the periodograms
    points_per_peak = 5
    periodogram_grid_resolution = points_per_peak*max_freq*baseline # frequency resolution of the periodograms

    # RESULS DIRECTORY

    results_dir = "/home/astro/kbarbey/pdm/products/HERMES/" # directory of the results



    # Preprocess the spectra

    for i in obs_data.time_series.vals:
        if abs(min_wv-max_wv) >= 100:
            i = i.InterpolateSpectrum()
            i = i.FilterSpectrum(lowcut=3, highcut=0.15, order = 1)
            i = i.ApplyCosineBell(alpha=0.3)
        else:
            i = i.InterpolateSpectrum()

    # Rearrange the RVs with the spectra

    obs_data.rearrange_time_series(rv=rv, times=times,ids=ids,unique_id = True)

    ## Compute periodograms

    # Choosing frequency range and frequency resolution for the periodograms.
    obs_data.initialize_periodicity_detector(freq_range=freq_range,
                                            periodogram_grid_resolution=periodogram_grid_resolution)

    obs_data.periodicity_detector.calc_GLS()

    print("GLS done",flush=True)

    obs_data.periodicity_detector.calc_PDC(calc_biased_flag=False, calc_unbiased_flag=True)

    print("PDC done",flush=True)

    obs_data.periodicity_detector.calc_USURPER(calc_biased_flag=False, calc_unbiased_flag=True)

    print("USURPER done",flush=True)

    obs_data.periodicity_detector.calc_partial_periodogram(partial_type="shape")

    print("Shape done",flush=True)

    obs_data.periodicity_detector.calc_partial_periodogram(partial_type="shift")

    print("Shift done",flush=True)

    # Save the observations instance in a pickle file with the name of the spec_dir name in the results directory

    with open(os.path.join(results_dir, f"{spec_dir.rsplit('/',maxsplit=1)[-1]}_{str(min_wv)}_{str(max_wv)}.csv"), 'w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["freq", "gls","usurper","pdc_unbiased","shape_periodogram", "shift_periodogram"])
        for i in range(len(obs_data.periodicity_detector.results_frequency['GLS'])):
            writer.writerow([obs_data.periodicity_detector.results_frequency['GLS'][i],
                            obs_data.periodicity_detector.results_power['GLS'][i],
                            obs_data.periodicity_detector.results_power['USURPER'][i],
                            obs_data.periodicity_detector.results_power['PDC_unbiased'][i],
                            obs_data.periodicity_detector.results_power['shape_periodogram'][i],
                            obs_data.periodicity_detector.results_power['shift_periodogram'][i]]
                            )

print("Done")
