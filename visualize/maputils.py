import numpy as np


# Function to get color based on a value and percentiles
def get_color(value, q25, q50, q75, low_color, mid_color, high_color):
    if value > q75:
        return high_color
    elif value > q50:
        return mid_color
    elif value > q25:
        return low_color
    else:
        return [255, 100, 0] 


# Function to add color based on a specified column using percentiles
def add_color_to_data(data, column, low_color, mid_color, high_color):
    values = data[column]
    q25, q50, q75 = np.percentile(values, [25, 50, 75])

    if column == 'rating':
        data["color"] = data[column].apply(
            lambda x: get_color(x, 3, 4, 4.5, low_color, mid_color, high_color)
        )
    else:
        data["color"] = data[column].apply(
            lambda x: get_color(x, q25, q50, q75, low_color, mid_color, high_color)
        )
