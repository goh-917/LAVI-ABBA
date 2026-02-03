import pickle
import matplotlib.pyplot as plt

'''This script load and visualise the LFP channel recordings continuously'''

class InteractiveVisualizer:
    def __init__(self, base_path, file_indices, colors, window_size=2000000000):
        """
        Initialize the interactive visualizer.

        Parameters:
        - base_path (str): Path to the directory containing the pickle files.
        - file_indices (list): List of file indices to visualize.
        - colors (list): List of colors for each dataset.
        - window_size (int): Number of data points to display at a time.
        """
        self.base_path = base_path
        self.file_indices = file_indices
        self.colors = colors
        self.window_size = window_size
        self.current_start = 0
        self.data_list = []
        self.tetrode = 'BLA good channels'
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Load all data
        self.load_all_data()

        # Plot the initial data
        self.update_plot()

        # Connect the key press event
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def load_data(self, file_path):
        """Load data from a pickle file."""
        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
            return data
        except EOFError:
            print(f"Error: The file {file_path} is empty or corrupted.")
            return None
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def load_all_data(self):
        """Load data from all specified files."""
        for i, file_index in enumerate(self.file_indices):
            file_name = f"{file_index}.pickle"
            file_path = self.base_path + file_name
            data = self.load_data(file_path)
            if data is not None:
                print(f"Loaded data from {file_path}, type: {type(data)}, length: {len(data)}")
                self.data_list.append((data, file_name, self.colors[i % len(self.colors)]))

    def update_plot(self):
        """Update the plot with the current window of data."""
        self.ax.clear()  # Clear the current plot
        start = self.current_start
        end = start + self.window_size
        print(f"Displaying data window: {start} to {end}")
        for data, label, color in self.data_list:
            if start < 0:  # Prevent negative indexing
                start = 0
                end = self.window_size
            if start >= len(data):  # Skip if start index exceeds data length
                continue
            self.ax.plot(data[start:end], label=label, color=color, alpha=0.7)
        self.ax.set_title(self.tetrode)
        self.ax.set_xlabel('Time (ms)')
        self.ax.set_ylabel('LFP amplitude (µV)')
        self.ax.legend(title='File Names', loc='lower left')
        self.ax.grid(True)
        self.fig.canvas.draw()  # Redraw the figure

    def on_key_press(self, event):
        """Handle key press events to navigate through data."""
        if event.key == 'l':  # Move forward
            self.current_start += self.window_size
            print(f"Pressed 'l': Moving to the next window")
            self.update_plot()
        elif event.key == 'a':  # Move backward
            self.current_start -= self.window_size
            if self.current_start < 0:  # Prevent going before the start of data
                self.current_start = 0
            print(f"Pressed 'a': Moving to the previous window")
            self.update_plot()


# Usage
base_path = '/Users/claudiagoh/Desktop/Course directory/RP1/dataset/R14/habituation/'
file_indices = [66, 68, 72, 77, 80, 90, 92, 105]  # Specify the indices of the files you want to visualize
colors = ['b', 'g', 'r', 'c', 'pink', 'purple', 'orange', 'grey']  # Colors for each dataset

# Initialize the interactive visualizer
visualizer = InteractiveVisualizer(base_path, file_indices, colors)

# Show the interactive plot
plt.show()
