import os
import re

def rename_files_in_folder(folder_path):
    """Rename files in the specified folder to remove prefixes and keep only the number."""
    # List all files in the specified folder
    for file_name in os.listdir(folder_path):
        # Use a regex to find the number in the filename
        match = re.match(r'cleaned_lfp_channel_(\d+)\.pickle', file_name)
        if match:
            # Extract the number from the filename
            number = match.group(1)
            # Construct the new file name
            new_file_name = f"cleaned_{number}.pickle"
            # Create full paths for the old and new file names
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_file_name)
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {old_file_path} -> {new_file_path}')

def main():
    # Specify the folder containing the files to rename
    folder_path = '/Users/claudiagoh/Desktop/Course directory/RP1/cleaned_data/r14/habituation'  

    # Call the rename function
    rename_files_in_folder(folder_path)

if __name__ == "__main__":
    main()  # Execute the main function when the script is run
