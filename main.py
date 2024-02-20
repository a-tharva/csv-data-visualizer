import csv
import matplotlib.pyplot as plt

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

sorted_unique_values = sorted(unique_values_dict.items(), key=lambda x: len(x[1]))

line_number = 0
for column_name, unique_values in sorted_unique_values:
    print(f"{line_number} Column '{column_name}' has {len(unique_values)} unique value(s):")
    line_number += 1
    # print(unique_values)



# Get user input for columns to plot
columns_to_plot_str = input("Enter the numbers of the columns you want to plot (comma-separated): ")
columns_to_plot_indices = [int(i) for i in columns_to_plot_str.split(",")]


# Create subplots for the pie charts
# fig, axs = plt.subplots(1, unique_values_required, figsize=(unique_values_required, unique_values_required))


# j = 2 if len(axs)%2 == 0 else 3
# n=0
# # Plot a pie chart for each column
# for i, (column_name, unique_values) in enumerate(columns_to_plot):
#     # Count the occurrences of each unique value
#     value_counts = {value: 0 for value in unique_values}
#     with open(csv_file_path, mode='r') as file:
#         csv_reader = csv.reader(file)
#         next(csv_reader)  # Skip the header row
#         for row in csv_reader:
#             if row[columns.index(column_name)] in value_counts:
#                 value_counts[row[columns.index(column_name)]] += 1
    

#     # Plot the pie chart
#     axs[i,].pie(value_counts.values(), labels=value_counts.keys(), autopct='%1.1f%%', startangle=140)
#     axs[i,].set_title(f"{column_name}")

# # Adjust layout
# plt.tight_layout()
# # i=0
# # for name in sorted_unique_values[:unique_values_required]:
# #     print(i)
# #     btn = Button(axs[i], f'{name}')
# #     i +=1

# # Show the plot
# plt.show()


# fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.3)

# # Plot all pie charts on the same plot
# patches = []
# for i, (column_name, unique_values) in enumerate(columns_to_plot):
#     # Count the occurrences of each unique value
#     value_counts = {value: 0 for value in unique_values}
#     with open(csv_file_path, mode='r') as file:
#         csv_reader = csv.reader(file)
#         next(csv_reader)  # Skip the header row
#         for row in csv_reader:
#             if row[columns.index(column_name)] in value_counts:
#                 value_counts[row[columns.index(column_name)]] += 1

#     # Plot the pie chart
#     patches.extend(ax.pie(value_counts.values(), labels=value_counts.keys(), autopct='%1.1f%%', startangle=140, visible=False))

# # Create check buttons for each column
# rax = plt.axes([0.05, 0.4, 0.2, 0.15])
# labels = [f"Column '{column_name}'" for column_name, _ in columns_to_plot]
# check = CheckButtons(rax, labels, [False] * len(columns_to_plot))

# # Function to toggle visibility of pie chart
# def toggle_visible(label):
#     index = labels.index(label)
#     patches[index*2].set_visible(not patches[index*2].get_visible())
#     patches[index*2+1].set_visible(not patches[index*2+1].get_visible())
#     plt.draw()

# # Connect check buttons to function
# check.on_clicked(toggle_visible)

# # Set title
# ax.set_title('Unique Values Distribution')

# # Show the plot
# plt.show()


# Calculate the number of rows and columns for subplots
num_rows = (len(columns_to_plot_indices) + 1) // 2  # Add 1 to round up
num_cols = 2

# Create subplots
fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
axs = axs.flatten()  # Flatten the 2D array of axes for easier indexing

# Plot pie charts
for i, idx in enumerate(columns_to_plot_indices):
    column_name, unique_values = sorted_unique_values[idx]
    # Count the occurrences of each unique value
    value_counts = {value: 0 for value in unique_values}
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row[columns.index(column_name)] in value_counts:
                value_counts[row[columns.index(column_name)]] += 1

    # Plot the pie chart
    patches, texts = axs[i].pie(value_counts.values(), startangle=140)
    axs[i].set_title(f"Column '{column_name}'")
    # Add legend with percentages
    legend_labels = [f"{label} ({value_counts[label] * 100 / sum(value_counts.values()):.1f}%)"
                     for label in value_counts.keys()]
    axs[i].legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))



# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()