# 1,2,3,4,5,7

import csv
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

csv_file_path = "data.csv"


unique_values_dict = {}

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)


    columns = next(csv_reader)
    print(columns)

    for column_name in columns:
        unique_values_dict[column_name] = []


    for row in csv_reader:
        for i, value in enumerate(row):
            if value not in unique_values_dict[columns[i]]:
                unique_values_dict[columns[i]].append(value)

# Sort the dictionary by the number of unique values in each column
sorted_unique_values = sorted(unique_values_dict.items(), key=lambda x: len(x[1]))

# Display the columns and their unique value counts
for i, (column_name, unique_values) in enumerate(sorted_unique_values):
    print(f"{i} Column '{column_name}' has {len(unique_values)} unique value(s)")

# Get user input for columns to plot
columns_to_plot_str = input("Enter the numbers of the columns you want to plot (comma-separated): ")
columns_to_plot_indices = [int(i) for i in columns_to_plot_str.split(",")]

# Calculate the number of rows and columns for subplots
num_rows = (len(columns_to_plot_indices) + 1) // 2  # Add 1 to round up
num_cols = 2

# Create subplots
fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
axs = axs.flatten()  # Flatten the 2D array of axes for easier indexing

# Initialize filtered data to be the full data
filtered_data = []
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        filtered_data.append(row)

orig_filtered_data = filtered_data

# Dictionary to store radio buttons for each column
radio_buttons = {}

def get_column_name_from_unique_value(unique_value):
    for column_name, unique_values in unique_values_dict.items():
        if unique_value in unique_values:
            return column_name
    return None  # Return None if the unique value is not found in any column


# Function to update the plot based on the selected filter
def update_plot(label):
    global filtered_data
    if label == 'Filter':
        # Filter the data based on the selected unique value
        for column_name, radio_button in radio_buttons.items():
            if isinstance(radio_button, RadioButtons) and radio_button.value_selected != 'None':
                print(f'---filtering with {column_name} for selected {radio_button.value_selected}')
                column_name = get_column_name_from_unique_value(radio_button.value_selected)
                column_idx = columns.index(column_name)
                filtered_data = [row for row in filtered_data if row[column_idx] == radio_button.value_selected]
            else:
                print(f'---not filtering with {column_name} for selected {radio_button.value_selected}')
    else:
        filtered_data = [row for row in orig_filtered_data]

    choices = []
    height = 0
    # Plot pie charts and create/update radio buttons
    for i, idx in enumerate(columns_to_plot_indices):
        column_name, unique_values = sorted_unique_values[idx]
        # Count the occurrences of each unique value
        value_counts = {value: 0 for value in unique_values}
        for row in filtered_data:
            if row[columns.index(column_name)] in value_counts:
                value_counts[row[columns.index(column_name)]] += 1

        # Clear previous pie chart
        axs[i].clear()
        # Plot the pie chart
        if not value_counts:
            continue
        print(f'--drawing chart with {value_counts.values()} and lables {value_counts.keys()}')
        patches, texts = axs[i].pie(value_counts.values(), startangle=140)
        axs[i].set_title(f"Column '{column_name}'")
        # Add legend with percentages
        legend_labels = [f"{label} ({value_counts[label] * 100 / sum(value_counts.values()):.1f}%)"
                         for label in value_counts.keys()]
        axs[i].legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Get the position of the current pie chart
        pos = axs[i].get_position()
        height += pos.height
        # Create/update radio buttons for filtering by unique values
        choices += list(value_counts.keys())
            
    choices += ['None']
    render_buttons(choices, height)

    # Adjust layout
    plt.tight_layout()
    # Update the plot
    plt.draw()

def render_buttons(choices: list, height: int) -> None:
    if column_name not in radio_buttons:
        rax = fig.add_axes([0.02, 0.01, 0.1, height/2])
        
        radio = RadioButtons(rax, choices)
        radio.set_active(choices.index('None'))  # Select 'None' by default
        radio.on_clicked(lambda column_name=column_name: filter_by_value(column_name))
        # radio.on_clicked(filter_by_value(column_name))
        radio_buttons[column_name] = radio
    else:
        pass
        # radio_buttons[column_name].labels = ['None'] + list(value_counts.keys())
        # radio_buttons[column_name].set_active(choices.index('None'))


# Function to filter data by selected unique value
def filter_by_value(column_name):
    # global filtered_data
    # if label != 'None':
    #     filtered_data = [row for row in filtered_data if row[columns.index(column_name)] == label]
    # else:
    #     filtered_data = [row for row in filtered_data]
    # update_plot('Filter')  # Redraw the plot with the new filtered data
    pass

# Create radio buttons for 'Filter' and 'No Filter'
# left, bottom, width, height values
rax = plt.axes([0.02, 0.8, 0.1, 0.15])
radio = RadioButtons(rax, ['No Filter','Filter'])
radio.on_clicked(update_plot)

# Update the plot initially
update_plot('No Filter')

# Show the plot
plt.show()