# The original LAVI toolbox
The LAVI toolbox is used to generate rhythmicity profile and automatic band detection of electrophysiological neural data. It is developed and first introduced in Karvat et al. (2024), Universal rhythmic architecture uncovers distinct modes of neural dynamics    
LAVI quantifies the rhythmicity of the neural signal by comparing phase coherence at a fixed time lag
ABBA distinguish neural activity into sustained and transient bands (activity with significantly high and low rhythmicity)

# The LAVI-ABBA toolbox
This LAVI-ABBA toolbox made some adjustments from the original LAVI tool, including:
1. 100 PINK noises are generated per recording channel, rather than 20 repetitions
2. average LAVI and PINK noise across epochs
