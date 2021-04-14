import numpy as np
from typing import Dict, Callable
import logging


log = logging.getLogger(__name__)


def channel_r(rgb_array: np.array) -> np.array:
    temp_array = np.array([1, 0, 0])
    new_array = rgb_array * temp_array
    return new_array


def channel_g(rgb_array: np.array) -> np.array:
    temp_array = np.array([0, 1, 0])
    new_array = rgb_array * temp_array
    return new_array


def channel_b(rgb_array: np.array) -> np.array:
    temp_array = np.array([0, 0, 1])
    new_array = rgb_array * temp_array
    return new_array


def channel_rg(rgb_array: np.array) -> np.array:
    temp_array = np.array([1, 1, 0])
    new_array = rgb_array * temp_array
    return new_array


def channel_rb(rgb_array: np.array) -> np.array:
    temp_array = np.array([1, 0, 1])
    new_array = rgb_array * temp_array
    return new_array


def channel_gb(rgb_array: np.array) -> np.array:
    temp_array = np.array([0, 1, 1])
    new_array = rgb_array * temp_array
    return new_array


def channel_rgb(rgb_array: np.array) -> np.array:
    temp_array = np.array([1, 1, 1])
    new_array = rgb_array * temp_array
    return new_array


def channel_function(rgb_array: np.array, channel_string: str) -> np.array:
    """
    Apply channel mask to pixels of image to work with channel.

    Args:
         rgb_array: Numpy array of image pixels.
         channel_string: Channel that to work.

    Returns:
        New array of image pixels that to work.
    """
    log.info('Choose image channel')
    map_to_channel: Dict[str, Callable[[tuple], tuple]] = {
        'R': channel_r,
        'G': channel_g,
        'B': channel_b,
        'RG': channel_rg,
        'RB': channel_rb,
        'GB': channel_gb,
        'RGB': channel_rgb
    }
    log.info('The channel was chose.')
    return map_to_channel.get(channel_string, channel_rgb)(rgb_array)
