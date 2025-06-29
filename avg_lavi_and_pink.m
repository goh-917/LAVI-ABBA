%Averaged LAVI values and PINK noise across epochs

%Add the LAVI toolbox to your Matlab path
% Construct LAVI path
LAVIpath = '/Users/claudiagoh/Desktop/MATLAB/LAVI-main'; % Location of the LAVI toolbox
addpath(LAVIpath); % Add the toolbox to the MATLAB path

%Load raw data
%Data should contain a matrix with N_chan x N_timepoints preprocessed data, and the sampling frequency in Hz.
% Construct the .mat path
dataFileName = fullfile(LAVIpath, 'LAVI_results',  'HPC', '4 min epoch', 'r14:qw40:lavi:pink.mat'); % Path to saved data

% Load the .mat file
loaded_file = load(dataFileName);

% Check the structure of the loaded results
disp('Loaded structure fields:');
disp(fieldnames(loaded_file));
disp(loaded_file.PINK_matrix);
disp(size(loaded_file.PINK_matrix))
PINK_matrix = loaded_file.PINK_matrix
disp(loaded_file.LAVI_matrix);
disp(size(loaded_file.LAVI_matrix))
LAVI_matrix = loaded_file.LAVI_matrix

%Average LAVI values across epochs 
%There are total of 8 channels, each channel produces x number epochs (differ between brain states), each epoch contain 96 LAVI values. 
%Now, we want to calculate the average of those LAVI values across epochs.
%Hence at the end, this section should produce 96 LAVI value per channel.
% Initialize variables
num_channels = size(LAVI_matrix, 1); % Number of channels, default=8
LAVI_values = size(LAVI_matrix, 2);  % Number of LAVI values per epoch, default=96 (same as foi)
num_epochs = size(LAVI_matrix, 3);   % Number of epochs, differ between brain states


% Initialize an array to hold the average LAVI values
avg_LAVI_values = zeros(num_channels, LAVI_values); % Preallocate for efficiency

% Loop through all channels and compute the average LAVI values
for channel_idx = 1:num_channels
    % Access the current channel of the LAVI_matrix
    LAVI_ch = LAVI_matrix(channel_idx, :, :);
    
    % Calculate the average LAVI values across epochs
    avg_LAVI = mean(LAVI_ch, 3); % Average across the third dimension (epochs)
    
    % Store the average LAVI values for the current channel
    avg_LAVI_values(channel_idx, :) = avg_LAVI; 
end

% Display the average LAVI values
disp(avg_LAVI_values);

%Averaging PINK values
% Initialize variables
num_pink_noise = size(PINK_matrix, 1);  % Number of PINK values per epoch, default=100 (same as foi)
num_freq = size(PINK_matrix, 2);  % Number of LAVI values per epoch, default=96 (same as foi)
num_channels = size(PINK_matrix, 3); % Number of channels, default=8
num_epochs = size(PINK_matrix, 4);   % Number of epochs, differ between brain states

PINK_matrix

% Initialize an array to hold the average LAVI values
avg_PINK_values = zeros(num_pink_noise, num_freq, num_channels); % Preallocate for efficiency

% Averaging across epochs (4th dimension)
for channel_idx = 1:num_channels
    % Extract all reps/freqs/epochs for current channel
    channel_data = PINK_matrix(:, :, channel_idx, :);
    
    % Average across epochs (4th dim) - squeeze removes singleton dim
    avg_PINK_values(:, :, channel_idx) = mean(channel_data, 4);
end

% Display the average LAVI values
disp('Average PINK noise values:');
disp(size(avg_PINK_values));

Saving averaged LAVI values and PINK noise
outputFileName = fullfile(LAVIpath, 'LAVI_results','HPC', '4 min epoch avg','qw_avg.mat');
LAVI_avg = avg_LAVI_values
PINK_avg = avg_PINK_values

% Save the combined PINK_matrix to the .mat file
save(outputFileName, 'LAVI_avg','PINK_avg'); % Append PINK_matrix to the existing file

