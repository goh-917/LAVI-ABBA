import numpy as np
from scipy.io import savemat, loadmat

def convert_npy_to_mat(npy_file_path, mat_file_path):
    """Convert a .npy file to a .mat file and verify the conversion."""
    try:
        # Load the .npy file
        data = np.load(npy_file_path, allow_pickle=True)
        print("Loaded data from .npy file:")
        print(data)
        print("Data type:", type(data))

        # Save the data to a .mat file
        savemat(mat_file_path, {'data': data})  # 'data' is the variable name in the .mat file
        print(f"Data saved successfully as {mat_file_path}")

        # Verify the conversion by loading the .mat file
        loaded_data = loadmat(mat_file_path)['data']
        
        # Check if the original and loaded data are the same
        if np.array_equal(data, loaded_data):
            print("Conversion verification successful: Data matches.")
        else:
            print("Conversion verification failed: Data does not match.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
npy_file_path = "/Users/claudiagoh/Desktop/Course directory/RP1/saved_matrices/PFC/r14_habituation_rem.npy"  # Replace with your .npy file path
mat_file_path = "/Users/claudiagoh/Desktop/Course directory/RP1/saved_matrices/PFC/r14_habituation_rem.mat"  # Desired .mat file path
convert_npy_to_mat(npy_file_path, mat_file_path)

