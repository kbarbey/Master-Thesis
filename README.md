# Project description

Cepheids are pulsating stars whose radius and brightness vary within a stable period. This feature is particularly important in astrometry since it allows us to measure their distance accurately. And consequently, use them as standard candles to calibrate the cosmic distance ladder. However, many other effects other than their pulsation can modify the incoming signals from these stars, such as the presence of an orbiting star. In these cases, the spectra, and therefore the measured radial velocity, of the Cepheid will contain information from both phenomena that can be complicated to distinguish.

 The aim of this project is to explore a newly developed methodology that could allow us to determine the pulsation and orbit periods of binary Cepheids without using any prior knowledge. This method constructs periodograms calculated using the concept of partial distance correlation, which allows us to effectively distinguish the Doppler shifts due to orbital motion and the spectral line variability induced by the stellar activity.

In this project, the student will work with part of the python package SPARTA and apply it to real study cases. The student will study the limitations and strong points of this method. Understand the precision and accuracy of the results. Propose modifications or improvements to the technique and experiment with them.

# Project progress

## Week 1 :  

1. Read articles : Binnenfeld et al. (2021), Anderson(2018) and Székely, Izzo(2016)
2. Set up SPARTA code -> some dependencies problems with python 3.7. Requirements.txt needs to be updated. 
    1. Works with python 3.8 though. 

    2. Had to change code in USURPER.py because lists are not accepted in nopython mode of numba. Changed them to numpy objects instead.

    3. Trying the examples and tutorials.
