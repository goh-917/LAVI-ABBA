import os
import pickle
import re
import pandas as pd

'''This script creates a dataframe by assigning the tetrode to the channel maps. 
It includes the following components:
1. File: store pickle files as strings
2. Area: store brain regions
3. Tetrode: store the tetrode number
4. Leads: store the channel order (1st-4th) in the tetrode
This dataframe is saved in the file named assigned_dataframe '''


def load_channel_map(animal):
    file_path = os.path.join("/Users/claudiagoh/Desktop/Course directory/RP1/channel_maps/ChMaps", f"{animal}.pickle")
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def load_condition_data(base_path, animal, condition):
    folder_path = os.path.join(base_path, f"dataset/{animal}/{condition}")
    condition_data = {}
    
    files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.pickle')],
        key=lambda x: int(re.match(r'(\d+)\.pickle', x).group(1))
    )

    for file_name in files:
        index = int(re.match(r'(\d+)\.pickle', file_name).group(1))
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'rb') as file:
            condition_data[(animal, index)] = pickle.load(file)
    
    return condition_data

def assign_condition_data(channel_map, condition_data, animal):
    assigned_data = []
    for index, channel in enumerate(channel_map):
        data = condition_data.get((animal, index))
        if data is not None:
            assigned_data.append({'Channel': channel, 'File': f"{index}.pickle"})
    return pd.DataFrame(assigned_data)

def transform_dataframe(assigned_df):
    assigned_df['Area'] = assigned_df['Channel'].str.split('TT').str[0].str.strip()
    assigned_df['Tetrode'] = assigned_df['Channel'].str.extract(r'(TT\d+)')[0]
    assigned_df['Leads'] = (assigned_df.index % 4) + 1
    return assigned_df[['File', 'Area', 'Tetrode', 'Leads']]

def save_assigned_data(animal, condition, transformed_data):
    save_folder = '/Users/claudiagoh/Desktop/Course directory/RP1/assigned_dataframe'
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, f"{animal}_{condition}_assigned.pickle")
    with open(save_path, 'wb') as file:
        pickle.dump(transformed_data, file)
    print(f"Saved assigned data for {animal} ({condition}) at: {save_path}")


def main():
    animals = ["r14"] # 'r16', 'r19', 'r20']
    conditions = ['habituation'] #'fear_conditioning', 'probe_testing', 'extinction_training', 'extinction_testing']
    base_path = '/Users/claudiagoh/Desktop/Course directory/RP1'

    for animal in animals:
        channel_map = load_channel_map(animal)
        
        for condition in conditions:
            condition_data = load_condition_data(base_path, animal, condition)
            assigned_data = assign_condition_data(channel_map, condition_data, animal)

            # Transform the DataFrame
            transformed_data = transform_dataframe(assigned_data)
            print(transformed_data)      
            save_assigned_data(animal, condition, transformed_data)

if __name__ == "__main__":
    main()
