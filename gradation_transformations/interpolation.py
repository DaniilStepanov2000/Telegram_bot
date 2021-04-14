import pathlib
import logging
from typing import Callable
from config import Settings

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.interpolate import interp1d


log = logging.getLogger(__name__)


def get_inter_image(image_path: pathlib.Path, inter_func: interp1d, settings: Settings, user_id: int) -> pathlib.Path:
    """Create linear interpolated image.

    Args:
         image_path: Path where saved image.
         inter_func: Linear interpolation function.
         settings: Contains main settings.
         user_id: User id that send message.

    Returns:
        Path where saved linear interpolated image.
    """
    image = Image.open(image_path)
    array = np.uint16(np.asarray(image))
    temp = inter_func(array)
    np.putmask(temp, temp > 255, 255)
    new_image = Image.fromarray(np.uint8(temp))
    new_image_path = settings.project_static_path / f'{user_id}_f_inter.jpg'
    new_image.save(new_image_path)
    return new_image_path


def get_interpolation(x_list: list, y_list: list, user_id: int, settings: Settings) -> (str, str, Callable):
    """Process linear interpolation.

    Args:
        x_list: Coordinates on the axis X.
        y_list: Coordinates on the axis Y.
        user_id: User id that send message.
        settings: Contains main settings.

    Returns:
        Tuple that contains paths where saved plot with coordinates, plot with linear
        interpolation and linear interpolation function.
    """
    log.info('Start create plots with coordinates and liner interpolation!')
    x = np.asarray(x_list)
    y = np.asarray(y_list)
    f = interp1d(x, y)
    plt.plot(x, y, 'o')
    plt.axis([-2, 257, -2, 257])
    path_points = settings.project_static_path / f'{user_id}_points.jpg'
    plt.savefig(path_points)
    path_plot = settings.project_static_path / f'{user_id}_plot.jpg'
    plt.plot(x, y, 'o', x, f(x), '-')
    plt.savefig(path_plot)
    plt.clf()
    log.info('Plots was successful created!')
    return path_points, path_plot, f


def separate_coordinates(test_list: list) -> (list, list):
    new_coordinates = list(map(int, test_list))
    test_x_coordinates = []
    test_y_coordinates = []
    for i in range(len(new_coordinates)):
        if i % 2 == 0:
            test_x_coordinates.append(new_coordinates[i])
        else:
            test_y_coordinates.append(new_coordinates[i])
    return test_x_coordinates, test_y_coordinates


def begin_draw_plots(
        string: str,
        image_path: pathlib.Path,
        user_id: int,
        settings: Settings,
) -> (str, str, str):
    """Process interpolation part.

    Args:
        string: Coordinates.
        image_path: Path where saved image.
        user_id: User id that send message.
        settings: Contains main settings.

   Returns:
       Tuple that contains paths for plot with coordinates, plot with
       linear interpolation and path where saved result image.
    """
    log.info('Start interpolation part')

    list_string = string.split(" ")
    x_cor, y_cor = separate_coordinates(list_string)
    points_path, plot_path, inter_f = get_interpolation(x_cor, y_cor, user_id, settings)
    inter_path_picture = get_inter_image(image_path, inter_f, settings, user_id)

    log.info('The interpolation part was successful')
    return points_path, plot_path, inter_path_picture
