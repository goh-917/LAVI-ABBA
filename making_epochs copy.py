import os
import pickle
import numpy as np
import warnings
from scipy.io import savemat

warnings.filterwarnings("ignore", category=DeprecationWarning)

def load_specific_lfp_data(dataset_folder, specific_files):
    '''Load LFP data from specified pickle files.'''
    lfp_data_list = []
    
    for file_name in specific_files:
        file_path = os.path.join(dataset_folder, f'{file_name}.pickle') 
        print (file_path) 

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                lfp_data = pickle.load(file)
            lfp_data_list.append(lfp_data)
        else:
            print(f'File not found: {file_path}')

    return lfp_data_list

def load_sleep_scores(sleep_score_path):
    '''Load sleep score for a specified animal and condition, duplicating each score 5000 times.'''
    with open(sleep_score_path, 'rb') as file:
        data = pickle.load(file)
    
    array_data = data[-1]
    sleep_scores = [float(score) for score in array_data for _ in range(5000)]
    return sleep_scores

def load_and_process_audio_timestamps(file_path):
    '''Load audio timestamps from a pickle file and convert them to integers.'''
    with open(file_path, 'rb') as file:
        timestamps = pickle.load(file)

    audio_timestamps = [int(ts) for sound_list in timestamps for ts in sound_list]
    return audio_timestamps

def mark_data_with_stimuli(lfp_data, audio_timestamps):
    '''Replace 3000 data points in LFP data with 'x' at each audio stimulus timestamp.'''
    marked_lfp = np.array(lfp_data, dtype=object)

    for stimulus_time in audio_timestamps:
        start_index = stimulus_time  # Convert to zero-based index
        if start_index + 3000 <= len(marked_lfp):
            marked_lfp[start_index:start_index + 3000] = ['x'] * 3000
        else:
            print(f"Warning: Not enough data points to replace at index {start_index}.")
    return marked_lfp

def assign_data_with_sleepscore(marked_lfp, sleep_scores):
    """Segment LFP data based on sleep scores."""
    assigned_marked_lfp = {}
    num_sleep_scores = len(sleep_scores)
    
    for i in range(len(marked_lfp)):
        if i < num_sleep_scores:
            score = sleep_scores[i]
            if i not in assigned_marked_lfp:
                assigned_marked_lfp[i] = {'score': score, 'data': []}
            assigned_marked_lfp[i]['data'].append(marked_lfp[i])
        else:
            if i not in assigned_marked_lfp:
                assigned_marked_lfp[i] = {'score': None, 'data': []}
            assigned_marked_lfp[i]['data'].append(marked_lfp[i])

    return assigned_marked_lfp

def group_data(assigned_marked_lfp):
    """Group segments based on sleep scores and concatenate data."""
    
    groups = {
        'REM': {'count': 0, 'data': []},
        'Unidentified': {'count': 0, 'data': []},  
    }
    
    unassigned_count = 0

    for index, items in assigned_marked_lfp.items():
        score = items['score']
        if score == 4:  # Only REM
            groups['REM']['count'] += 1
            groups['REM']['data'].extend(items['data'])
        else:
            groups['Unidentified']['count'] += 1
            groups['Unidentified']['data'].extend(items['data'])

    for group in groups:
        groups[group]['total_data_points'] = len(groups[group]['data'])

    return groups, unassigned_count

def remove_x_values(groups):
    """Remove data points equal to 'x' from each brain state group and retain original indices."""
    for group in groups:
        original_indices = [i for i, value in enumerate(groups[group]['data']) if value != 'x']
        groups[group]['data'] = [value for value in groups[group]['data'] if value != 'x']
        groups[group]['total_data_points'] = len(groups[group]['data'])
        groups[group]['original_indices'] = original_indices  # Store original indices
    return groups

def create_and_save_epochs(lfp_data_list, audio_timestamps, sleep_scores, save_folder, animal_id, condition):
    """Create and save multiple epochs of REM data, each lasting 2 minutes (120,000 data points)."""
    epoch_length = 240000  # 4 minutes of data points
    epoch_count = 0  # Counter for the number of epochs created

    all_epochs_per_channel = []  # List to store all short epochs from each good channel

    # Process data for each specified channel
    for idx, lfp_data in enumerate(lfp_data_list):
        print(f'Processing data from channel with index {idx}:')

        marked_lfp = mark_data_with_stimuli(lfp_data, audio_timestamps)  
        assigned_marked_lfp = assign_data_with_sleepscore(marked_lfp, sleep_scores)
        brain_state_groups, unassigned_count = group_data(assigned_marked_lfp)
        brain_state_groups = remove_x_values(brain_state_groups)

        rem_data = brain_state_groups['REM']['data']
        original_indices = brain_state_groups['REM']['original_indices']

        # Create epochs for this channel
        consecutive_indices = []
        channel_epochs = []  # Store the epochs for this channel

        for i in range(len(rem_data)):
            if rem_data[i] != 'x':
                consecutive_indices.append(original_indices[i])
                # Check if we have enough consecutive data points
                if len(consecutive_indices) == epoch_length:
                    epoch_data = rem_data[i - epoch_length + 1:i + 1]  # Last 120000 data points
                    channel_epochs.append(epoch_data)  # Add the epoch to the list for this channel
                    epoch_count += 1
                    consecutive_indices = []  # Reset for the next epoch
            else:
                consecutive_indices = []  # Reset if 'x' is encountered

        all_epochs_per_channel.append(channel_epochs)  # Store epochs for this channel

    # Check if all channels have the same number of epochs
    num_epochs_per_channel = len(all_epochs_per_channel[0])  # Number of epochs in the first channel
    for epochs in all_epochs_per_channel:
        if len(epochs) != num_epochs_per_channel:
            print("Warning: Not all channels have the same number of epochs.")
            return

    # Now create the matrices, where each matrix contains the corresponding epochs from all channels
    for epoch_index in range(num_epochs_per_channel):
        matrix_data = []

        for channel_epochs in all_epochs_per_channel:
            matrix_data.append(channel_epochs[epoch_index])  # Add the same epoch from each channel

        # Save the matrix (e.g., matrix 1, matrix 2, etc.)
        savemat(os.path.join(save_folder, f'{animal_id}_{condition}_matrix_{epoch_index}.mat'), {'matrix': matrix_data})
        print(f"Saved matrix {epoch_index} with corresponding epochs from all channels")

    print(f"Total epochs saved: {epoch_count}")

def main():
    base_path = '/Users/claudiagoh/Desktop/Course directory/RP1'
    animal_id = 'r14'
    condition = 'habituation'
    area = 'BLA'
    brain_state = 'REM'

    timestamps_path = os.path.join(base_path, 'audio_timestamps', f'{animal_id}_{condition}_sleep.pickle')
    sleep_score_path = os.path.join(base_path, 'sleep_score', f'{animal_id}_{condition}_sleep.pickle')
    dataset_folder = os.path.join(base_path, 'dataset', animal_id, condition)
    save_folder = os.path.join(base_path, 'saved_matrices', area, brain_state)
    os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist

    specific_files = ['66','68','72','77','80','90','93','105']  # Specify the pickle files you want to process
    lfp_data_list = load_specific_lfp_data(dataset_folder, specific_files)

    if lfp_data_list:
        sleep_scores = load_sleep_scores(sleep_score_path)
        audio_timestamps = load_and_process_audio_timestamps(timestamps_path)

        # Call the function to create and save REM epochs
        create_and_save_epochs(lfp_data_list, audio_timestamps, sleep_scores, save_folder, animal_id, condition)

    else:
        print('No LFP data to process.')
        return  # Exit if no LFP data

if __name__ == '__main__':
    main()
