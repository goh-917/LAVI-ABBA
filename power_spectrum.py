import matplotlib.pyplot as plt
from scipy.signal import welch
import pickle

# List of pickle file indices to plot
file_indices = [116, 117, 118, 119] 

# Corresponding colors for each file
colors = ['b', 'g', 'r', 'c']

# Base path to the pickle files
base_path = '/Users/claudiagoh/Desktop/Course directory/RP1/dataset/R14/habituation/'

# Set the sampling frequency (adjust as needed)
fs = 1000  

# Initialize the plot
plt.figure(figsize=(10, 6))

# Loop through each file, load the data, and plot
for file_index, color in zip(file_indices, colors):
    # Add '.pickle' extension to the file name
    file_name = f'{file_index}.pickle'
    
    # Construct the full file path
    file_path = f'{base_path}{file_name}'
    
    # Load the LFP data from the pickle file
    with open(file_path, 'rb') as file:
        lfp_data = pickle.load(file)
    
    # Apply Welch's method to estimate the PSD
    frequencies, psd_values = welch(lfp_data, fs, nperseg=1024)
    
    # Plot the PSD with a label corresponding to the file name and assign the color
    plt.semilogy(frequencies, psd_values, label=f'File {file_index}', color=color)

# Add plot title and labels
plt.title("Power Spectral Density (PSD):HPCTT20")
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (V^2/Hz)')

# Add legend to distinguish the plots
plt.legend()

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
