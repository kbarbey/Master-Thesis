How to open the .p files and what they contain:
1. Read

from pathlib import Path
import pandas as pd

file_path = Path('./RASSINE_CORALIE.2015-01-24T06_40_21.000.p')
rassine_spec = pd.read_pickle(file_path)

2. What they contain:

rassine_spec file keys:  dict_keys(['wave', 'flux', 'flux_used', 'output', 'parameters'])
rassine_spec["output"] keys:  dict_keys(['continuum_linear', 'anchor_wave', 'anchor_flux', 'anchor_index'])

See Cretignier(2020) and the Rassine code for details on each quantity.

3. Spectrum wavelengths and normalised flux values are given by:

wavelength = rassine_spec['wave']
normalised_flux = rassine_spec['flux']/rassine_spec['output']['continuum_linear']

N.B. : There is also a 'continuum_cubic' but I didn't compute it because of time/computational constraints and Cretignier(2020) argued that the linear continuum gives better results in almost all cases.