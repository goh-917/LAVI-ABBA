%Combine Matrices
%This script combines epochs into a big matrix
%LAVI values from different epochs are combined into LAVI_matrix
%PINK values from different epochs are combined into PINK_matrix

%Initialised combined matrices
PINK_matrix = zeros(100, 65, 5, 6); % pink noises=100, foi=96, channels=8, epochs=n
LAVI_matrix = zeros(5, 65, 6) % channels=8, foi=96, epochs=n

%Make LAVI and PINK Matrices
for i = 0:5 % Loop from file 0 to file n-1 
    dataFileName = fullfile(LAVIpath, '4 min all LAVI', 'HPC', 'QW',sprintf('matrix%d.mat', i));
    loaded_struct = load(dataFileName);
    
    % Check the structure of the loaded results
    disp('Loaded structure fields:');
    disp(fieldnames(loaded_struct));
    disp(loaded_struct.results)


    PINK_matrix(:, :, :, i+1) = loaded_struct.results.PINK
    LAVI_matrix(:, :, i+1) = loaded_struct.results.LAVI


    % Debugging: Check if the data is being saved correctly
    disp(['File ', num2str(i), ':']);
    disp(['PINK matrix size: ', num2str(size(PINK_matrix(:, :, :, i + 1)))]);
    disp(['PINK first element: ', num2str(PINK_matrix(1, 1, 1, i + 1))]); % Accessing the first element correctly
    
   
end

% After the loop, load the existing file and update the LAVI_matrix
outputFileName = fullfile(LAVIpath, 'LAVI_results', 'HPC', '4 min epoch','r14:qw40:lavi:pink.mat');

% Check if the file exists
if ~isfile(outputFileName)
    % If the file does not exist, create an empty .mat file
    save(outputFileName, 'LAVI_matrix'); % You can initialize LAVI_matrix as needed
end

data = load(outputFileName);

% Save the whole LAVI_matrix back to the file
data.LAVI_matrix = LAVI_matrix; % Update the entire matrix
save(outputFileName, '-struct', 'data');



%Save Matrices
% Save the combined PINK_matrix to the .mat file
save(outputFileName, 'PINK_matrix', '-append'); % Append PINK_matrix to the existing file

