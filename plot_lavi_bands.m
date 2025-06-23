% Plot the significantly sustained bands detected by ABBA
figure(647); clf; hold on
set(gcf,'position',[680 400 800 600]);

% Plot the LAVI values
plot(foi, LAVI, 'k-', 'LineWidth', 1.5);

% Plot the significantly sustained bands
for chi = 1:size(LAVI,1)
    % Get the band information for the current channel
    bands = borders2{chi};
    
    % Plot the significantly sustained bands
    for i = 1:size(bands,1)
        if bands(i,11) % Check if the band is significant (Sig column)
            if bands(i,9) == 1 % Check if the band is a peak (Dir column)
                plot([bands(i,4) bands(i,5)], [bands(i,7) bands(i,7)], 'g-', 'LineWidth', 3);
            end
        end
    end
end

% Set axis labels and title
xlabel('Frequency (Hz)');
ylabel('LAVI value');
title('Significantly Sustained Bands');

% Set log scale for x-axis
set(gca, 'XScale', 'log', 'XTick', [2:2:10, 20:10:foi(end)]);
xlim([0.5, 120]);
