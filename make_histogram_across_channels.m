%Make Histogram Across Channels
%This script creates histograms, which shows the distribution of sustained and transient bands across brain regions and states (fraction of channel)
% Define paths for the four states
states = {'aw', 'qw', 'nrem', 'rem'}; % State names
num_states = length(states);
dataFileNames = cell(num_states, 1);

% Construct the .mat paths for all states
for i = 1:num_states
    dataFileNames{i} = fullfile(LAVIpath, 'LAVI_results', 'A1', '4 min epoch avg', [states{i} '_avg.mat']);
end

% Load the .mat files
LAVI_matrices = cell(num_states, 1);
SigVect_matrices = cell(num_states, 1);

for i = 1:num_states
    loaded_file = load(dataFileNames{i});
    LAVI_matrices{i} = loaded_file.LAVI_avg;
    SigVect_matrices{i} = vertcat(loaded_file.sigVect2{:});
end

% Initialize variables for plotting
num_frequencies = size(LAVI_matrices{1}, 2);
colors = {[0.1250 0.5625 0.9375], [1.0000 0.4980 0.0549], [0.1765 0.6275 0.1765], [0.8392 0.1529 0.1608]}; % Muted color palette


%Sustained Bands Analysis
sig_percentage_all = zeros(num_states, num_frequencies);

% Loop through all frequency bins and compute the percentage of significant channels for each state
for state_idx = 1:num_states
    LAVI_matrix = LAVI_matrices{state_idx};
    SigVect_matrix = SigVect_matrices{state_idx};
    
    for freq_idx = 1:num_frequencies
        LAVI_freq = LAVI_matrix(:, freq_idx);
        SigVect_freq = SigVect_matrix(:, freq_idx);
        
        num_channels = size(LAVI_freq, 1); % number of channels 
        sig_channel = sum(SigVect_freq > 0, 1); % Count significant channels (SUSTAINED)
        sig_percentage_all(state_idx, freq_idx) = sig_channel / num_channels * 100; % Store percentage
    end
end

% Plot overlapping sustained bands
figure('Position', [100 100 800 600]);
hold on;

for state_idx = 1:num_states
    semilogx(foi, sig_percentage_all(state_idx, :), 'LineWidth', 2, 'Color', colors{state_idx}, 'DisplayName', upper(states{state_idx}));
end

xlabel('Frequency (Hz)', 'FontSize', 14);
set(gca, 'XTick', [1 2 4 6 8 10 20 40], ...
    'XTickLabel', {'1', '2', '4', '6', '8', '10', '20', '40'}, 'FontSize', 12);

ylabel('Sustained bands (fraction of channels)', 'FontSize', 14);
title('Distribution of Sustained Bands Across Brain States: A1', 'FontSize', 14);

ylim([0 105]);
xlim([0.8 42]);
set(gca, 'XScale', 'log'); % Force logarithmic scale
grid on;
legend('show', 'Location', 'northeastoutside', 'FontSize', 12);

% Create subplots for sustained bands
figure('Position', [100 100 1200 800]);

for state_idx = 1:num_states
    subplot(2, 2, state_idx);
    
    semilogx(foi, sig_percentage_all(state_idx, :), 'LineWidth', 2, 'Color', colors{state_idx});
    
    xlabel('Frequency (Hz)', 'FontSize', 12);
    set(gca, 'XTick', [1 2 4 6 8 10 20 40], ...
        'XTickLabel', {'1', '2', '4', '6', '8', '10', '20', '40'}, 'FontSize', 10);
    
    ylabel('Sustained bands (%)', 'FontSize', 12);
    title(sprintf('%s', upper(states{state_idx})), 'FontSize', 14, 'FontWeight', 'bold');
    
    ylim([0 105]);
    xlim([0.8 42]); 
    grid on;
    set(gca, 'FontSize', 10);
end

sgtitle('Distribution of Sustained Bands Across Brain States: A1', 'FontSize', 16, 'FontWeight', 'bold');

%Transient Bands Analysis
sig_percentage_all = zeros(num_states, num_frequencies); % Reinitialize for transient bands

% Loop through all frequency bins and compute the percentage of significant channels for each state
for state_idx = 1:num_states
    LAVI_matrix = LAVI_matrices{state_idx};
    SigVect_matrix = SigVect_matrices{state_idx};
    
    for freq_idx = 1:num_frequencies
        LAVI_freq = LAVI_matrix(:, freq_idx);
        SigVect_freq = SigVect_matrix(:, freq_idx);
        
        num_channels = size(LAVI_freq, 1); % number of channels = 8
        sig_channel = sum(SigVect_freq < 0, 1); % Count significant channels (TRANSIENT)
        sig_percentage_all(state_idx, freq_idx) = sig_channel / num_channels * 100; % Store percentage
    end
end

% Plot overlapping transient bands
figure('Position', [100 100 800 600]);
hold on;

for state_idx = 1:num_states
    semilogx(foi, sig_percentage_all(state_idx, :), 'LineWidth', 2, 'Color', colors{state_idx}, 'DisplayName', upper(states{state_idx}));
end

xlabel('Frequency (Hz)', 'FontSize', 14);
set(gca, 'XTick', [1 2 4 6 8 10 20 40], ...
    'XTickLabel', {'1', '2', '4', '6', '8', '10', '20', '40'}, 'FontSize', 12);

ylabel('Transient bands (fraction of channels)', 'FontSize', 14);
title('Distribution of Transient Bands Across Brain States: A1', 'FontSize', 14);

ylim([0 105]);
xlim([0.8 42]);
set(gca, 'XScale', 'log'); % Force logarithmic scale
grid on;
legend('show', 'Location', 'northeastoutside', 'FontSize', 12);

% Create subplots for transient bands
figure('Position', [100 100 1200 800]);

for state_idx = 1:num_states
    subplot(2, 2, state_idx);
    
    semilogx(foi, sig_percentage_all(state_idx, :), 'LineWidth', 2, 'Color', colors{state_idx});
    
    xlabel('Frequency (Hz)', 'FontSize', 12);
    set(gca, 'XTick', [1 2 4 6 8 10 20 40], ...
        'XTickLabel', {'1', '2', '4', '6', '8', '10', '20', '40'}, 'FontSize', 10);
    
    ylabel('Transient bands (%)', 'FontSize', 12);
    title(sprintf('%s', upper(states{state_idx})), 'FontSize', 14, 'FontWeight', 'bold');
    
    ylim([0 105]);
    xlim([0.8 42]);
    grid on;
    set(gca, 'FontSize', 10);
end

sgtitle('Distribution of Transient Bands Across Brain States: A1', 'FontSize', 16, 'FontWeight', 'bold');

