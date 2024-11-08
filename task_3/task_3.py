import numpy as np

def time_to_cyclic(hour):
    radians = (hour / 24) * 2 * np.pi
    sin_time = np.sin(radians)
    cos_time = np.cos(radians)
    return sin_time, cos_time
