import os
import pickle
import pandas as pd
from sparta.Observations import Observations

# Specify the parent directory containing all the folders
SPEC_DIR = "/home/astro/kbarbey/pdm/S1D/spectra"
RV_DIR = "/home/astro/kbarbey/pdm/S1D/RV"

# List all subdirectories (folders) in the parent directory
SPEC_FOLD = sorted([os.path.join(SPEC_DIR,folder) for folder in os.listdir(SPEC_DIR)
                    if os.path.isdir(os.path.join(SPEC_DIR, folder))])
RV_FOLD = sorted([os.path.join(RV_DIR,folder) for folder in os.listdir(RV_DIR)])
print(SPEC_FOLD,RV_FOLD)
# Loop over all subdirectories
for rv_folder, spectra_folder in zip(RV_FOLD, SPEC_FOLD):

    # DATA PARAMETERS

    SURVEY = "CORALIE" # survey name
    SAMPLE_RATE= 1 # sample rate of the data
    MIN_WV = 4000 # minimum wavelength of the data
    MAX_WV = 6000 # maximum wavelength of the data
    spec_dir = spectra_folder # directory of the spectra
    rv_dir = rv_folder # directory of the RVs

    # LOAD DATA

    obs_data = Observations(survey=SURVEY, sample_rate=SAMPLE_RATE, min_wv=MIN_WV, max_wv=MAX_WV,
                            target_visits_lib=SPEC_DIR)
    df = pd.read_csv(rv_dir)
    rv = df.rv.astype(float).values
    e_rv = df.rv_err.astype(float).values
    times = df.bjd.astype(float).values
    times = times - int(min(times))

    # PERIODOGRAM PARAMETERS

    baseline = int(obs_data.time_series.times[-1])
    MIN_FREQ = 1/1000 # Or maybe 1/2/baseline to be sure but let's test it that way.
    MAX_FREQ = 1/2 # we don't expect more than one pulsation every two day so should be alright.
    freq_range = (MIN_FREQ, MAX_FREQ) # frequency range of the periodograms
    PPP = 5 # points per peak
    periodogram_grid_resolution = PPP*MAX_FREQ*baseline # frequency resolution of the periodograms

    # RESULS DIRECTORY

    RESULTS_DIR = "/home/astro/kbarbey/pdm/S1D/results" # directory of the results



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

    # Save the observations instance in a pickle file with the name of 
    # the spec_dir name in the results directory

    file = open(os.path.join(RESULTS_DIR,
                             f"{spec_dir.rsplit('/',maxsplit=1)[-1]}_{str(MIN_WV)}_{str(MAX_WV)}.pkl"), 'wb')
    pickle.dump(obs_data, file)
    file.close()

print("Done")
