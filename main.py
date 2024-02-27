# 1,2,3,4,5,7

import csv
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons


def load_csv_data(csv_file_path: str) -> tuple[list[str], dict[str, list[str]]]:
    """Load data from a CSV file and return column names and unique values for each column.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        Tuple[List[str], Dict[str, List[str]]]: A tuple containing a list of column names and a dictionary
        mapping each column name to its list of unique values.
    """
    unique_values_dict = {}
    with open(csv_file_path, mode="r") as file:
        csv_reader = csv.reader(file)
        columns = next(csv_reader)
        for column_name in columns:
            unique_values_dict[column_name] = []
        for row in csv_reader:
            for i, value in enumerate(row):
                if value not in unique_values_dict[columns[i]]:
                    unique_values_dict[columns[i]].append(value)
    return columns, unique_values_dict


def get_column_name_from_unique_value(
    unique_value: str, unique_values_dict: dict[str, list[str]]
) -> str:
    """Get the column name corresponding to a unique value.

    Args:
        unique_value (str): The unique value to find the column name for.
        unique_values_dict (Dict[str, List[str]]): A dictionary mapping column names to their unique values.

    Returns:
        str: The column name corresponding to the unique value, or an empty string if not found.
    """
    for column_name, unique_values in unique_values_dict.items():
        if unique_value in unique_values:
            return column_name
    return ""


def update_plot(label: str) -> None:
    """Update the plot based on the selected filter.

    Args:
        label (str): The label of the radio button clicked ('Filter' or 'No Filter').
    """
    global filtered_data, orig_filtered_data
    if label == "Filter":
        for column_name, radio_button in radio_buttons.items():
            if (
                isinstance(radio_button, RadioButtons)
                and radio_button.value_selected != "None"
            ):
                column_name = get_column_name_from_unique_value(
                    radio_button.value_selected, unique_values_dict
                )
                column_idx = columns.index(column_name)
                filtered_data = [
                    row
                    for row in filtered_data
                    if row[column_idx] == radio_button.value_selected
                ]
    else:
        filtered_data = [row for row in orig_filtered_data]

    choices = []
    height = 0
    for i, idx in enumerate(columns_to_plot_indices):
        column_name, unique_values = sorted_unique_values[idx]
        value_counts = {value: 0 for value in unique_values}
        for row in filtered_data:
            if row[columns.index(column_name)] in value_counts:
                value_counts[row[columns.index(column_name)]] += 1
        axs[i].clear()
        if not value_counts:
            continue
        patches, texts = axs[i].pie(value_counts.values(), startangle=140)
        axs[i].set_title(f"Column '{column_name}'")
        legend_labels = [
            f"{label} ({value_counts[label] * 100 / sum(value_counts.values()):.1f}%) - {value_counts[label]}"
            for label in value_counts.keys()
        ]
        axs[i].legend(
            patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)
        )
        pos = axs[i].get_position()
        height += pos.height
        choices += list(value_counts.keys())
    choices += ["None"]
    render_buttons(choices, height)

    plt.tight_layout()
    plt.draw()


def render_buttons(choices: list[str], height: int) -> None:
    """Render radio buttons for filtering.

    Args:
        choices (List[str]): The list of choices for the radio buttons.
        height (int): The height of the radio button axes.
    """
    if column_name not in radio_buttons:
        rax = fig.add_axes([0.02, 0.01, 0.1, height / 2])
        radio = RadioButtons(rax, choices)
        radio.set_active(choices.index("None"))  # Select 'None' by default
        radio.on_clicked(lambda column_name=column_name: filter_by_value(column_name))
        radio_buttons[column_name] = radio


def filter_by_value(column_name: str) -> None:
    """Filter data by selected unique value.

    Args:
        column_name (str): The name of the column to filter by.
    """
    pass


csv_file_path = input("Enter path to csv file: ")
columns, unique_values_dict = load_csv_data(csv_file_path)
sorted_unique_values = sorted(unique_values_dict.items(), key=lambda x: len(x[1]))
print("Unique values in each column:")
for i, (column_name, unique_values) in enumerate(sorted_unique_values):
    print(f"{i} Column '{column_name}' has {len(unique_values)} unique value(s)")

columns_to_plot_str = input(
    "Enter the numbers of the columns you want to plot (comma-separated): "
)
columns_to_plot_indices = [int(i) for i in columns_to_plot_str.split(",")]

num_rows = (len(columns_to_plot_indices) + 1) // 2
num_cols = 2

fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
axs = axs.flatten()

filtered_data = []
with open(csv_file_path, mode="r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        filtered_data.append(row)

orig_filtered_data = filtered_data
radio_buttons = {}

rax = plt.axes([0.02, 0.8, 0.1, 0.15])
radio = RadioButtons(rax, ["No Filter", "Filter"])
radio.on_clicked(update_plot)

update_plot("No Filter")
plt.show()
