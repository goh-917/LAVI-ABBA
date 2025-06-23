# The original LAVI toolbox
The LAVI toolbox is used to generate rhythmicity profile and automatic band detection of electrophysiological neural data. It is developed and first introduced in Karvat et al. (2024), Universal rhythmic architecture uncovers distinct modes of neural dynamics    
LAVI quantifies the rhythmicity of the neural signal by comparing phase coherence at a fixed time lag
ABBA distinguish neural activity into sustained and transient bands (activity with significantly high and low rhythmicity)

# The LAVI-ABBA toolbox
This LAVI-ABBA toolbox made some adjustments from the original LAVI tool, including:
1. 100 PINK noises are generated per recording channel, rather than 20 repetitions
2. average LAVI and PINK noise across epochs

# References
When using this toolbox please cite the following publications:

1. Karvat, G., Crespo-García, M., Vishne, G., Anderson, M. & Landau, A. N. Universal rhythmic architecture uncovers distinct modes of neural dynamics. 2024.12.05.627113 Preprint at https://doi.org/10.1101/2024.12.05.627113 (2024).
2. Oostenveld, R., Fries, P., Maris, E. & Schoffelen, J.-M. FieldTrip: Open Source Software for Advanced Analysis of MEG, EEG, and Invasive Electrophysiological Data. Intell. Neuroscience 2011, 1:1-1:9 (2011).
3. Venema, V., Ament, F. & Simmer, C. A Stochastic Iterative Amplitude Adjusted Fourier Transform algorithm with improved accuracy. Nonlinear Processes in Geophysics 13, 321–328 (2006).
