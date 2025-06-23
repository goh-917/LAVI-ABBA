% Calculate LAVI values and PINK noise
% This script calculate LAVI values and 100 pink noise per channel, across the frequency of interest

% Load Raw Data
% Add LAVI toolbox to your MATLAB path
LAVIpath = '/Users/claudiagoh/Desktop/MATLAB/LAVI-main'; % Location of the LAVI toolbox
addpath(LAVIpath); % Add the toolbox to the MATLAB path


% Frequencies of interest and other parameters
foi         = 10.^(log10(1):0.025:log10(40)); % frequencies of interest
fsample     = 1000;              % sampling frequency
lag         = 1.5;               % lag between the signal and its copy (in cycles, default = 1.5)
width       = 5;                 % wavelet width (in cycles, default = 5)
pink_reps   = 100;               % number of simulations created per channel. Default = 20.

% Number of Files (epochs)
numFiles    = 6;                % Number of files to process


%Calculate LAVI and generate 100 pink noise and save matrix
%The actual calculation of LAVI is done with the function Prepare_LAVI.
%It assumes two inputs: cfg (the configuration structure), and the data. Data has to be a matrix (size: channel x timepoints). Can be empty ([]), and then default values are assigned (for default values, see the documantation of Prepare_LAVI). 
%The first output is the rhythmicity measure LAVI, as N_channels x N_frequencies.
%The second output, cfg, can be used to monitor which default values were assgined by the function.
%Pink noise can be generated with the function computePinkLAVI
% Loop through each file
for fileIndex = 0:numFiles-1
    % Construct the .mat path for each file
    dataFileName = fullfile(LAVIpath, 'saved_matrices/HPC/4 minute epochs/QW', sprintf('r14_habituation_matrix_%d.mat', fileIndex)); 
    
    % Load the .mat file
    loaded_struct = load(dataFileName);
    
    % Access the 'data' field
    myData = loaded_struct.matrix; % Ensure 'data' is a field in your loaded structure
    disp(['Processing file: ', dataFileName]);
    
    % Check dimensions and type
    disp(size(myData)); % Display the size of the data matrix
    disp(class(myData)); % Display the class/type of the data 
    durs = size(myData, 2) / fsample;  % the duration (in seconds) of each simulation
    choi = 1:size(myData, 1); % choose your channels of interest

    % Calculate LAVI of the data
    cfg = [];
    cfg.foi     = foi;
    cfg.fs      = fsample;
    cfg.lag     = lag;
    cfg.width   = width;
    cfg.verbose = 1;

    dat = myData(choi, :); % the original data was saved in a format similar to Fieldtrip
    if any(isnan(dat(:))); warning('Data contains NaNs. Calculating TFR by convolution in the time domain'); end
    [LAVI, cfg] = Prepare_LAVI(cfg, dat);

    % Generate pink noise matching the data and calculate its LAVI
    cfg = [];
    cfg.Pink_reps = pink_reps;  % number of repetitions (pink-noise instantiations)
    cfg.durs      = durs;       % duration of each simulation, in seconds
    cfg.foi       = foi;        % frequencies of interest

    PINK = computePinkLAVI(cfg, dat(choi, :)); % dimord: rep_freq_chan

    % Saving Results (LAVI, PINK)
    % Define the output file path
    outputFile = fullfile(LAVIpath, '4 min all LAVI', 'HPC','QW', sprintf('matrix%d.mat', fileIndex)); % Output file name

    % Initialize a matrix to hold LAVI values and PINK noise
    numChannels = size(LAVI, 1);
    LAVI_matrix = zeros(numChannels,size(LAVI,2)); % For LAVI values
    PINKMatrix = zeros(cfg.Pink_reps, size(LAVI, 2), numChannels); % For PINK values
    
 

    % Fill the matrices with LAVI and PINK data
    for chi = 1:numChannels
        LAVI_matrix(chi, :) = LAVI(chi, :); % Save LAVI for the current channel
        PINKMatrix(:, :, chi) = PINK(:, :, chi); % Save PINK for the current channel
    end

   

    % Create a structure to hold the results
    results.PINK = PINKMatrix; % Matrix of PINK values
    results.LAVI = LAVI_matrix; % Matrix of PINK values

    % Save the results structure to a single .mat file
    save(outputFile, 'results');

    disp(['LAVI and PINK results saved successfully in: ', outputFile]);
end

