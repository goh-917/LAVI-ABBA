import os
import pickle
import pandas as pd

'''This script labels the quality of tetrode data and update the dataframe with a new column named Quality.'''

def load_assigned_data(animal, condition):
    """
    Load assigned tetrode data from a pickle file for the specified animal and condition.
    Returns A DataFrame containing the assigned data, or None if the file is not found.
    """
    file_path = os.path.join("/Users/claudiagoh/Desktop/Course directory/RP1/assigned_dataframe", f"{animal}_{condition}_assigned.pickle")
    
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"Error: The file for {animal} under condition '{condition}' was not found.")
        return None

def label_quality(assigned_df, good_quality_indices):
    """
    Add a 'Quality' column to the DataFrame based on good quality indices.
    Returns the updated DataFrame with the 'Quality' column.
    """
    # Create a new column 'Quality' based on whether the index is in the good quality list
    assigned_df['Quality'] = assigned_df['File'].apply(
        lambda filename: 'Good' if int(filename.split('.')[0]) in good_quality_indices else 'Bad'
    )
    return assigned_df

def save_quality_data(animal, condition, assigned_df):
    """
    Save the updated DataFrame back to the original pickle file.
    """
    file_path = os.path.join("/Users/claudiagoh/Desktop/Course directory/RP1/assigned_dataframe", f"{animal}_{condition}_assigned.pickle")
    with open(file_path, 'wb') as file:
        pickle.dump(assigned_df, file)
    print(f"Updated data saved for {animal} under condition '{condition}'.")

def main():
    # Define the animal and good quality indices
    animal = "r14"
    condition = 'habituation'
    good_quality_indices = [0, 4, 9, 13, 16, 20, 24, 28, 34, 36, 42, 45, 
                            48, 52, 56, 60, 66, 68, 72, 77, 80, 84, 
                            90, 92, 96, 101, 105, 111, 112, 118, 122, 125]

    # Load the assigned data
    assigned_data = load_assigned_data(animal, condition)

    if assigned_data is not None:
        # Label the quality of the data
        labeled_data = label_quality(assigned_data, good_quality_indices)

        # Save the updated DataFrame back to the original file
        save_quality_data(animal, condition, labeled_data)

        # Display the updated DataFrame
        print(labeled_data)
    else:
        print("Data loading failed. Please check the file path and try again.")

if __name__ == "__main__":
    main()
