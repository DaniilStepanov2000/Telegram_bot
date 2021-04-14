import pathlib

import numpy as np
from PIL import Image, ImageOps
from config import Settings


def scale(first_list: np.array) -> np.array:
    r_min = np.min(first_list)
    r_max = np.max(first_list)

    t_min = 0
    t_max = 255

    new_list = ((first_list - r_min) / (r_max - r_min)) * (t_max - t_min) + t_min

    return new_list


def create_histogram(path_in_computer: str, settings: Settings, user_id: int) -> tuple:
    """Create channel histograms for the image.

    Args:
        path_in_computer: Path for image.
        settings: Contains main settings.
        user_id: User id that send message.

    Returns:
        Tuple that contains four paths for histograms.
    """
    first_image = Image.open(path_in_computer)
    r, g, b = first_image.split()

    r_array = r.histogram()
    g_array = g.histogram()
    b_array = b.histogram()

    new_r_array = scale(r_array)
    new_g_array = scale(g_array)
    new_b_array = scale(b_array)

    path_r = draw_histogram(new_r_array, f'{user_id}_lab_2_r_hist.jpg', settings, user_id)
    path_g = draw_histogram(new_g_array, f'{user_id}_lab_2_g_hist.jpg', settings, user_id)
    path_b = draw_histogram(new_b_array, f'{user_id}_lab_2_b_hist.jpg', settings, user_id)

    path_average = average_histogram(first_image, settings, user_id)

    all_paths = (path_r, path_g, path_b, path_average)
    return all_paths


def draw_histogram(array: np.array, name_file: str, settings: Settings, user_id: int) -> pathlib.Path:
    """Draw histogram.

    Args:
        array: Numpy array of image pixels.
        name_file: File name.
        settings: Contains main settings.
        user_id: User id that send message.

    Returns:
        Object that contains path for created histogram.
    """
    height = 256
    width = 256
    color_draw = (0, 0, 0)
    if name_file == f'{user_id}_lab_2_r_hist.jpg':
        color_draw = (255, 0, 0)
    if name_file == f'{user_id}_lab_2_g_hist.jpg':
        color_draw = (0, 255, 0)
    if name_file == f'{user_id}_lab_2_b_hist.jpg':
        color_draw = (0, 0, 255)

    new_image = Image.new('RGB', (width, height), 'white')
    px_new_image = new_image.load()

    for i in range(width):
        for j in range(int(array[i])):
            px_new_image[i, j] = color_draw

    final_image = ImageOps.flip(new_image)
    path_image = settings.project_static_path / name_file
    final_image.save(path_image)
    return path_image


def average_histogram(first_image: Image.Image, settings: Settings, user_id: int) -> pathlib.Path:
    first_array = np.asarray(first_image)

    sum_array = np.sum(first_array, axis=2) // 3
    average_array = sum_array.ravel()

    start_array = np.zeros(256)
    for i in range(average_array.size):
        temp = average_array[i]
        start_array[temp] = start_array[temp] + 1

    new_array = scale(start_array)
    path_average = draw_histogram(new_array, f'{user_id}_lab_2_average.jpg', settings, user_id)

    return path_average
