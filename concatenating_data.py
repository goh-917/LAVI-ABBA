import os
import pickle
import numpy as np
import warnings
from scipy.io import savemat

warnings.filterwarnings("ignore", category=DeprecationWarning)

def load_good_lfp_data(dataframe_path, dataset_folder):
    '''Load the first good channel's LFP data and its timestamps from a pickle file.'''
    with open(dataframe_path, 'rb') as file:
        data = pickle.load(file)

    good_channels = data[(data['Quality'] == 'Good') & (data['Area'] == 'PFC')]
    if good_channels.empty:
        print('No good channels found.')
        return None, None

    lfp_data_list = []
    good_indices = []

    for good_index in good_channels.index:
        file_path = os.path.join(dataset_folder, f'{good_index}.pickle') 

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                lfp_data = pickle.load(file)
            lfp_data_list.append(lfp_data)
            good_indices.append(good_index) 
        else:
            print(f'File not found: {file_path}')

    return lfp_data_list, good_indices

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
        'Wakefulness': {'count': 0, 'data': []},
        'NREM': {'count': 0, 'data': []},
        'REM': {'count': 0, 'data': []},
        'Unidentified': {'count': 0, 'data': []},  
    }
    
    unassigned_count = 0

    for index, items in assigned_marked_lfp.items():
        score = items['score']
        if score in [1, 2]:  
            groups['Wakefulness']['count'] += 1
            groups['Wakefulness']['data'].extend(items['data'])
        elif score == 3:  
            groups['NREM']['count'] += 1
            groups['NREM']['data'].extend(items['data'])
        elif score == 4:  
            groups['REM']['count'] += 1
            groups['REM']['data'].extend(items['data'])
        elif score == 5:  
            groups['Unidentified']['count'] += 1
            groups['Unidentified']['data'].extend(items['data'])
        else:
            unassigned_count += len(items['data'])

    for group in groups:
        groups[group]['total_data_points'] = len(groups[group]['data'])

    return groups, unassigned_count

def remove_x_values(groups):
    """Remove data points equal to 'x' from each brain state group."""
    for group in groups:
        groups[group]['data'] = [value for value in groups[group]['data'] if value != 'x']
        groups[group]['total_data_points'] = len(groups[group]['data'])
    return groups
import os
import numpy as np

def create_and_save_matrices(lfp_data_list, good_indices, audio_timestamps, sleep_scores, save_folder, animal_id, condition):
    """Create matrices for Wakefulness, NREM, and REM, and save them to files."""
    # Initialize matrices for each state
    wakefulness_matrix = []
    nrem_matrix = []
    rem_matrix = []

    for idx, (lfp_data, good_index) in enumerate(zip(lfp_data_list, good_indices)):
        print(f'Processing data from channel with index {good_index}:')

        marked_lfp = mark_data_with_stimuli(lfp_data, audio_timestamps)  
        assigned_marked_lfp = assign_data_with_sleepscore(marked_lfp, sleep_scores)
        brain_state_groups, unassigned_count = group_data(assigned_marked_lfp)
        brain_state_groups = remove_x_values(brain_state_groups)

        # Append sample data to respective matrices
        wakefulness_matrix.append(brain_state_groups['Wakefulness']['data'])
        nrem_matrix.append(brain_state_groups['NREM']['data'])
        rem_matrix.append(brain_state_groups['REM']['data'])

        for group, info in brain_state_groups.items():
            print(f"""
            Group: {group},
            Total data points: {info['total_data_points']},
            Sample Data: {info['data'][:5]} 
            """)

        print(f"Total unassigned data points: {unassigned_count}")

    # Convert lists to NumPy arrays for matrix representation
    wakefulness_matrix = np.array(wakefulness_matrix, dtype=object)
    nrem_matrix = np.array(nrem_matrix, dtype=object)
    rem_matrix = np.array(rem_matrix, dtype=object)

    # Save matrices as .mat files
    #savemat(os.path.join(save_folder, f'{animal_id}_{condition}_wakefulness.mat'), {'wakefulness': wakefulness_matrix})
    savemat(os.path.join(save_folder, f'{animal_id}_{condition}_nrem.mat'), {'nrem': nrem_matrix})
    #savemat(os.path.join(save_folder, f'{animal_id}_{condition}_rem.mat'), {'rem': rem_matrix})

    print("Matrices saved successfully.")

def main():
    base_path = '/Users/claudiagoh/Desktop/Course directory/RP1'
    animal_id = 'r14'
    condition = 'habituation'
    area = 'A1'


    dataframe_path = os.path.join(base_path, 'assigned_dataframe', f'{animal_id}_{condition}_assigned.pickle')
    timestamps_path = os.path.join(base_path, 'audio_timestamps', f'{animal_id}_{condition}_sleep.pickle')
    sleep_score_path = os.path.join(base_path, 'sleep_score', f'{animal_id}_{condition}_sleep.pickle')
    dataset_folder = os.path.join(base_path, 'dataset', animal_id, condition)
    save_folder = os.path.join(base_path, 'saved_matrices', area)
    os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist

    lfp_data_list, good_indices = load_good_lfp_data(dataframe_path, dataset_folder)

    if lfp_data_list is not None:
        sleep_scores = load_sleep_scores(sleep_score_path)
        audio_timestamps = load_and_process_audio_timestamps(timestamps_path)

        # Call the function to create and save matrices
        create_and_save_matrices(lfp_data_list, good_indices, audio_timestamps, sleep_scores, save_folder, animal_id, condition)

    else:
        print('No LFP data to process.')
        return  # Exit if no LFP data

if __name__ == '__main__':
    main()


