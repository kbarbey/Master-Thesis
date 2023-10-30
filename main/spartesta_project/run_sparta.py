import os
import pandas as pd
import pickle
from sparta.Auxil.PeriodicityDetector import PeriodicityDetector
from sparta.UNICOR.Spectrum import Spectrum
from sparta.UNICOR.Template import Template
from sparta.Auxil.TimeSeries import TimeSeries
from sparta.Observations import Observations

# Specify the parent directory containing all the folders
spectra_directory = "/home/astro/kbarbey/pdm/S1D/spectra"
rv_directory = "/home/astro/kbarbey/pdm/S1D/RV"

# List all subdirectories (folders) in the parent directory
spectra_folders = sorted([os.path.join(spectra_directory,folder) for folder in os.listdir(spectra_directory) if os.path.isdir(os.path.join(spectra_directory, folder))])
rv_folders = sorted([os.path.join(rv_directory,folder) for folder in os.listdir(rv_directory)])
print(spectra_folders,rv_folders)
# Loop over all subdirectories
for rv_folder, spectra_folder in zip(rv_folders, spectra_folders):

    # DATA PARAMETERS

    survey = "CORALIE" # survey name
    sample_rate = 1 # sample rate of the data
    min_wv = 4000 # minimum wavelength of the data
    max_wv = 6000 # maximum wavelength of the data
    spec_dir = spectra_folder #"/home/astro/kbarbey/pdm/S1D/BGCru" # directory of the spectra
    rv_dir = rv_folder #"/home/astro/kbarbey/pdm/S1D/BGCru/RV/BG_Cru_coralie14.csv" # directory of the RVs

    # LOAD DATA

    obs_data = Observations(survey=survey, sample_rate=sample_rate, min_wv=min_wv, max_wv=max_wv,
                            target_visits_lib=spec_dir)
    df = pd.read_csv(rv_dir)
    rv = df.rv.astype(float).values
    e_rv = df.rv_err.astype(float).values
    times = df.bjd.astype(float).values
    times = times - int(min(times))

    # PERIODOGRAM PARAMETERS

    baseline = int(obs_data.time_series.times[-1])
    min_freq = 1/100 # Or maybe 1/2/baseline to be sure but let's test it that way.
    max_freq = 1/2 # we don't expect more than one pulsation every two day so should be alright.
    freq_range = (min_freq, max_freq) # frequency range of the periodograms
    points_per_peak = 5
    periodogram_grid_resolution = points_per_peak*max_freq*baseline # frequency resolution of the periodograms

    # RESULS DIRECTORY

    results_dir = "/home/astro/kbarbey/pdm/S1D/results" # directory of the results



    # Preprocess the spectra

    for i in obs_data.time_series.vals:
        i = i.SpecPreProccess()

    # Rearrange the RVs with the spectra

    obs_data.rearrange_time_series(rv=rv, times=times)

    ## Compute periodograms

    # Choosing frequency range and frequency resolution for the periodograms.
    obs_data.initialize_periodicity_detector(freq_range=freq_range,
                                            periodogram_grid_resolution=periodogram_grid_resolution)

    # obs_data.periodicity_detector.calc_GLS()

    # print("GLS done",flush=True)

    # obs_data.periodicity_detector.calc_PDC(calc_biased_flag=False, calc_unbiased_flag=True)

    # print("PDC done",flush=True)

    # obs_data.periodicity_detector.calc_USURPER(calc_biased_flag=False, calc_unbiased_flag=True)

    # print("USURPER done",flush=True)

    obs_data.periodicity_detector.calc_partial_periodogram(partial_type="shape")

    print("Shape done",flush=True)

    obs_data.periodicity_detector.calc_partial_periodogram(partial_type="shift")

    print("Shift done",flush=True)

    # Save the observations instance in a pickle file with the name of the spec_dir name in the results directory

    file = open(os.path.join(results_dir, f"{spec_dir.rsplit('/',maxsplit=1)[-1]}_{str(min_wv)}_{str(max_wv)}.pkl"), 'wb')
    pickle.dump(obs_data, file)
    file.close()

print("Done")
