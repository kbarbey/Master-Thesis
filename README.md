# Project description

Cepheids are pulsating stars whose radius and brightness vary within a stable period. This feature is particularly important in astrometry since it allows us to measure their distance accurately. And consequently, use them as standard candles to calibrate the cosmic distance ladder. However, many other effects other than their pulsation can modify the incoming signals from these stars, such as the presence of an orbiting star. In these cases, the spectra, and therefore the measured radial velocity, of the Cepheid will contain information from both phenomena that can be complicated to distinguish.

 The aim of this project is to explore a newly developed methodology that could allow us to determine the pulsation and orbit periods of binary Cepheids without using any prior knowledge. This method constructs periodograms calculated using the concept of partial distance correlation, which allows us to effectively distinguish the Doppler shifts due to orbital motion and the spectral line variability induced by the stellar activity.

In this project, the student will work with part of the python package SPARTA and apply it to real study cases. The student will study the limitations and strong points of this method. Understand the precision and accuracy of the results. Propose modifications or improvements to the technique and experiment with them.

# Project progress

## Week 1 :  

1. Read articles : Binnenfeld et al. (2021), Anderson(2018) and Székely, Izzo(2016)
2. Set up SPARTA code -> some dependencies problems with python 3.7. Requirements.txt needs to be updated. 
    1. Works with python 3.8.12 though and the following packages' versions:
    
    | Package                       | Version | Editable project location                             |
    | ----------------------------- | ------- | ---------------------------------------------------- |
    | astropy                       | 4.0.1.post1                                      |
    | asttokens                     | 2.4.0                                           |
    | atomicwrites                  | 1.3.0                                           |
    | attrs                         | 19.3.0                                          |
    | backcall                      | 0.2.0                                           |
    | backports.functools-lru-cache | 1.6.5                                           |
    | certifi                       | 2020.4.5.1                                     |
    | colorama                      | 0.4.3                                           |
    | comm                          | 0.1.4                                           |
    | cycler                        | 0.10.0                                          |
    | debugpy                       | 1.6.7                                           |
    | decorator                     | 5.1.1                                           |
    | easygui                       | 0.98.3                                          |
    | executing                     | 1.2.0                                           |
    | hypothesis                    | 5.5.4                                           |
    | importlib-metadata            | 1.5.0                                           |
    | ipykernel                     | 6.25.2                                          |
    | ipython                       | 8.12.0                                          |
    | jedi                          | 0.19.0                                          |
    | jupyter_client                | 8.3.1                                           |
    | jupyter_core                  | 5.3.2                                           |
    | kiwisolver                    | 1.1.0                                           |
    | llvmlite                      | 0.31.0                                          |
    | matplotlib                    | 3.1.3                                           |
    | matplotlib-inline             | 0.1.6                                           |
    | more-itertools                | 8.2.0                                           |
    | nest-asyncio                  | 1.5.6                                           |
    | numba                         | 0.48.0                                          |
    | numpy                         | 1.22.0                                          |
    | packaging                     | 20.3                                            |
    | pandas                        | 1.0.3                                           |
    | parso                         | 0.8.3                                           |
    | pickleshare                   | 0.7.5                                           |
    | pip                           | 23.2.1                                          |
    | platformdirs                  | 3.10.0                                          |
    | pluggy                        | 0.13.1                                          |
    | prompt-toolkit                | 3.0.39                                          |
    | psutil                        | 5.7.0                                           |
    | pure-eval                     | 0.2.2                                           |
    | py                            | 1.10.0                                          |
    | PyAstronomy                   | 0.14.0                                          |
    | Pygments                      | 2.16.1                                          |
    | pyparsing                     | 2.4.6                                           |
    | python-dateutil               | 2.8.1                                           |
    | pytz                          | 2019.3                                          |
    | pywin32                       | 305.1                                           |
    | pyzmq                         | 23.2.1                                          |
    | scipy                         | 1.4.1                                           |
    | setuptools                    | 68.0.0                                          |
    | six                           | 1.14.0                                          |
    | sortedcontainers              | 2.1.0                                           |
    | SPARTA                        | 0.1.0  | c:\users\kentb\desktop\pdm\sparta               |
    | stack-data                    | 0.6.2                                           |
    | tk                            | 0.1.0                                           |
    | tornado                       | 6.0.4                                           |
    | tqdm                          | 4.66.1                                          |
    | traitlets                     | 5.10.1                                          |
    | typing_extensions             | 4.8.0                                           |
    | wcwidth                       | 0.1.9                                           |
    | wheel                         | 0.41.2                                          |
    | wincertstore                  | 0.2                                             |
    | zipp                          | 2.2.0                                           |



    2. Had to change code in USURPER.py because lists are not accepted in nopython mode of numba. Changed them to numpy objects instead.

    3. Trying the examples and tutorials.

## Week 2 :

1. Problem in the code : shift periodogram doesn't match the one in the article. Comes from the USURPER_functions.py in the calc_pdc_unbiased function where the wavelength of the original spectra is shifted twice in the shift periodogram if the shape periodogram is called before the shift one. Workaround found by simply copying the wavelengths into a temporary variable.
2. TODO : 
    1. Play with the limits of the code, try to find some limiting factors. How does the code react to changing its parameters. For the moment still with SMus.
    2. Try to see how the uncertainties are defined and the p-values -> in Shen, 2021 it's only the distance correlation that we are talking about. Should the p-value be defined in an other way for pdc and spdc ?
    3. Try to start thinking in some way to automatise that shit. Finding the peaks automatically to infer if there is orbital motion or stellar activity and find the periods.
        1. Would it be a good idea to make some kind of ML algorithm to make the peak recognition more systematic and consistent ?
        -> talked with Edouard. Maybe try to find a simpler solution first. Pattern recognition or something similar. See k-nearest neighbour in ML course 2023. We'll need a predefined function to compare our peaks to it.
        2. Is there a rigorous way to define the p-values (probably, check Shen, 2021) and what would be the threshold to choose for this new method ? -> ML could give us a number
        3. How should a peak be characterised ? What's the height threshold to which we define that a peak is meaningful ? What would the peak shape mean ? Assume gaussian -> std is fwhm/2.355 ?
        
