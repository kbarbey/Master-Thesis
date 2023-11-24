# Project description

Cepheids are pulsating stars whose radius and brightness vary within a stable period. This feature is particularly important in astrometry since it allows us to measure their distance accurately. And consequently, use them as standard candles to calibrate the cosmic distance ladder. However, many other effects other than their pulsation can modify the incoming signals from these stars, such as the presence of an orbiting star. In these cases, the spectra, and therefore the measured radial velocity, of the Cepheid will contain information from both phenomena that can be complicated to distinguish.

 The aim of this project is to explore a newly developed methodology that could allow us to determine the pulsation and orbit periods of binary Cepheids without using any prior knowledge. This method constructs periodograms calculated using the concept of partial distance correlation, which allows us to effectively distinguish the Doppler shifts due to orbital motion and the spectral line variability induced by the stellar activity.

In this project, the student will work with part of the python package SPARTA and apply it to real study cases. The student will study the limitations and strong points of this method. Understand the precision and accuracy of the results. Propose modifications or improvements to the technique and experiment with them.

# Project progress

Contains everything on a weekly basis : what is done, what is to do, thoughts, ideas, insecurities, magical potion formula etc... 

Will evolve constantly until project is done. Then it will take a more official and concise form.

<font color="red">!!<font> -> important code change

## Week 1 :  

1. Read articles : Binnenfeld et al. (2021), Anderson(2018) and Székely, Izzo(2016)
2. <font color="red">!!<font> Set up SPARTA code -> some dependencies problems with python 3.7. Requirements.txt needs to be updated. 
    1. Works with python 3.8.12 though and the following packages' versions : see requirements.txt

    2. <font color="red">!!<font> Had to change code in `USURPER_functions.py` because lists are not accepted in `nopython` mode of numba. Changed them to numpy objects instead.

    3. Trying the examples and tutorials.

## Week 2 :

1. <font color="red">!!<font> Shift periodogram doesn't match the one in the article. Comes from the `USURPER_functions.py` in the `calc_pdc_unbiased` function where the wavelength of the original spectra is shifted twice in the shift periodogram if the shape periodogram is called before the shift one. Workaround found by simply copying the wavelengths into a temporary variable.
2. TODO : 
    1. Play with the limits of the code, try to find some limiting factors. How does the code react to changing its parameters. For the moment still with SMus.
    2. Try to see how the uncertainties are defined and the p-values -> in Shen, 2021 it's only the distance correlation that we are talking about. Should the p-value be defined in an other way for pdc and spdc ?
    3. Try to start thinking in some way to automatise that thing. Finding the peaks automatically to infer if there is orbital motion or stellar activity and find the periods.
        1. Would it be a good idea to make some kind of ML algorithm to make the peak recognition more systematic and consistent ?
        -> talked with Edouard. Maybe try to find a simpler solution first. Pattern recognition or something similar. See k-nearest neighbour in ML course 2023. We'll need a predefined function to compare our peaks to it.
        2. Is there a rigorous way to define the p-values (probably, check Shen, 2021) and what would be the threshold to choose for this new method ? -> ML could give us a number
        3. How should a peak be characterised ? What's the height threshold to which we define that a peak is meaningful ? What would the peak shape mean ? Assume gaussian -> std is fwhm/2.355 ?
        4. Check False-alarm rate(see other version of code on git), SNR($P_{peak}/P_{noise}$), statistical test (which one ?) Try to compute it.
            1. Binni computed the FAP using simple bootstrap method.
            2. Yeah compute the FAP and p-value using different methods-> Süveges made a nice comparative study (Suveges, 2015) where she compares the different methods to estimate the significance levels of peaks in periodograms : bootstrap(computationally expensive), Baluev(analytic but not always possible), GEV(hybrid between the formers), $F^M$(has a lot of caveats). <font color="red"> Would be nice to implement those maybe. Especially Baluev and GEV .<font>
            3. GEV would be really nice to have <font color="red">especially in our case where we have no prior information<font>(see intro of Suveges, 2014) IMPLEMENT GEV? (https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_genextreme.html)
3. Where in the spectrum should the RVs be computed ? Why 5800-6000A or 5600-5800 ?
4. Why did they change their code to compute the p-value and not the FAP anymore ? Anyway with both they get spurious(?) peaks above the 1e-4 line. But these peaks often appear in both shape and shift periodograms so maybe to detect them we could try to find if they appear in both. If that's the case at a certain level then they are probably spurious(need to check if reasonable).
5. Extracted rvs worked. The problem was that we had to account for air wv transformation in Coralie's RV computation.

## Week 3 :

After weekly meeting, we have a priority list I think :

1.	Test Henia's stars.
2.	Convergence test for complexity.
    1.	If O(Nlog(N)) then all good.
    2.	If not : think about how to make it happen.
3.	In parralel : 
    1.	Automatise the code for large data sets of RV(could be cool with VELOCE).
    2.	Make it work on Iestà.
    3.	Strong and weak points of the method : peak significance and peak aliases.
    4.	Interpretation of the periodogram. Uncertainties.

(3bis. O(Nlog(N)) if necessary.)

4.	About the maths themselves : metrics, correlated noise, Nyquist frequency, statistical power.

To code :

1. Find the peaks and their aliases.
2. Fold the Rvs to the main period found and plot it.
3. Compute the residuals.
4. Fold it to the second highest peak ?

Questions :

1. How should I pre-process the spectra ? What delta should I choose between the wv ? What parameters more generally ?
2. Is the shape variability of the spectrum different depending on where you're looking in it ? Because then I would argue that when loading the spectra, we should choose a range of wavelengths where the radial velocities were computed and not just randomly 5600-5800A.

## 24.10.2023 :

To Do :

1. Improve peak finding routine, cleaning of periodogram ? -> Done
3. Telluric (richard)
4. Wv ranges
5. Better examples(binaries) -> richard
6. In template.py, see air parameter(probably just refraction correction).

Plan on how to do it:

1. Peak finding routine:
    1. Periodogram cleaning:
        1. Finding the peaks: combine thresholding and simple height comparison of neighbouring points(adaptive thresholding). Why : Because usual threshold gives way too many peaks for even conservative p-values and simple height comparison doesn't work well in some case such as BG Crucis shape periodogram and V0391(lots of high fluctuations around highest peak).
        2. Find harmonics of the 2-3 highest and identify them(remove them also ? If yes, how ?)
        3. Do the same with harmonics of window functions. Search for $f=\text{days}^{-1}$ or even a week. See power spectrum of window function.
    2. Find peaks again(simple comparison should be ok now).
        1. Fit gaussian.
        2. Get best period + uncertainty
        3. Fold RVs accordingly.
        4. Get residuals by subtracting model again.
        5. Plot residuals.

## 12.11.2023 :

Done :

1. Peak finding routine is better. Still need to find a way to remove the harmonics of the window harmonics and window harmonics of harmonics. But that's not a priority.

Progress :

1. Tellurics: impossible to install Telfit or Molecfit on this computer. Tried really hard but windows is not made for that. Even on the VM I have problems. What could be done is to use Windows Linux Subsystem but for that I need more space of my SSD and I absolutely don't have it...

So the plan is the following : check manually for the moment the problematic zones and compare them to the ones where tellurics are less present or
even absent.

Problematic Absorption Zones:

    1. Huggins band : 3100-3400

    2. Chappuis band : 5000-7000 with peak at 6000

    3. O2 B-band : 6800-7000

    4. O2 A-band : 7600-7800

    5. Big H20 : 7100-7300

    6. Some Ozone in 4000-5000 range but minimal.

Above that, it's a mess. Once I have Molecfit or Telfit working, I'll try to compute a periodogram in a problematic zone by correcting each spectra -> ok no that's clearly too computationnally expensive.

2. Wv ranges : Computing errors as a function of range size but inside the 4000-5000 range.

To do:

1. Error: fit gaussian to the peak and get the error from the fit. Check if not easier to just use the formula from vanderplas,2018 since we know that $\sigma\propto\frac{1}{T}$.

2. Check all the other stars for telluric contamination and wavelength range.
Maybe plot power of the shape peak as a function of range size but that does change actually.

## Ideas:

1. Could we use these type of periodograms on FWHM and BIS ? For example, if BIS is stellar activity then maybe compute semi-partial distance correlation of BIS and RVs. Should be the same as shape and shift but BIS instead of CCF of two spectra. Maybe it's equivalent.

