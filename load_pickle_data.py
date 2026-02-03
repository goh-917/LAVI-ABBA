import pickle

path = '/Users/claudiagoh/Desktop/Course directory/RP1/assigned_dataframe/r14_habituation_assigned.pickle'

try:
    # Load the data from the pickle file
    with open(path, 'rb') as file:
        data = pickle.load(file)
    good_channels = data[(data['Quality'] == 'Good') & (data['Area'] == 'HPC')]

    print(good_channels)

    # Display the type and length of the data
    print(f"Type of data: {type(data)}")
    print(f"Length of data: {len(data)}")
    print(data[:])  # Display the first 10 elements if it's a list or similar structure

except EOFError:
    print("Error: The file is empty or corrupted.")
except Exception as e:
    print(f"An error occurred: {e}")

import os


