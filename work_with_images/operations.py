import pathlib
import logging
from typing import List, Tuple

import numpy as np
from PIL import Image
from aiogram.types import PhotoSize

from work_with_images.mask_operation import create_circle_mask, create_squared_mask, create_rectangle
from work_with_images.rgb_channel import channel_function
from typing import Optional


log = logging.getLogger(__name__)


def get_max_sized_photo(photos: List[PhotoSize]) -> PhotoSize:
    max_photo = photos[0]
    for photo in photos[1:]:
        if photo.width > max_photo.width:
            max_photo = photo

    return max_photo


def resize_pictures(first_image: Image.Image, second_image: Image.Image) -> Tuple[Image.Image, Image.Image]:
    """Resize pictures to the same size by biggest side.

    Args:
        first_image: First image to resize.
        second_image: Second image to resize.

    Returns:
        Two images with the same size by the biggest side.
    """
    first_size = first_image.size
    second_size = second_image.size
    result = (tuple(zip(first_size, second_size)))

    width = max(result[0])
    height = max(result[1])

    new_first_image = first_image.resize(tuple([width, height]))
    new_second_image = second_image.resize(tuple([width, height]))

    return new_first_image, new_second_image


def summation(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> Image.Image:
    """Perform  summation the pixels of two images.

    Args:
        first_image: First image for operation.
        second_image: Second image for operation.
        rgb_message: Channel that to work.

    Returns:
        One image that is result of performed operation.
    """
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.add(np.uint8(tuple_array_first), np.uint8(tuple_array_second), dtype=np.uint16)
    np.putmask(final_array, final_array > 255, 255)
    final_image = Image.fromarray(np.uint8(final_array))

    return final_image


def average(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> Image.Image:
    """Perform  arithmetic mean the pixels of two images.

    Args:
        first_image: First image for operation.
        second_image: Second image for operation.
        rgb_message: Channel that to work.

    Returns:
        One image that is result of performed operation.
    """
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.add(np.uint8(tuple_array_first), np.uint8(tuple_array_second), dtype=np.uint16) // 2
    np.putmask(final_array, final_array > 255, 255)
    final_image = Image.fromarray(np.uint8(final_array))

    return final_image


def maximum(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> Image.Image:
    """Find max values the pixels of two images.

        Args:
            first_image: First image for operation.
            second_image: Second image for operation.
            rgb_message: Channel that to work.

        Returns:
            One image that is result of performed operation.
    """
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.maximum(tuple_array_first, tuple_array_second)
    final_image = Image.fromarray(np.uint8(final_array))

    return final_image


def minimum(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> Image.Image:
    """Find min values the pixels of two images.

        Args:
            first_image: First image for operation.
            second_image: Second image for operation.
            rgb_message: Channel that to work.

        Returns:
            One image that is result of performed operation.
    """
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.minimum(tuple_array_first, tuple_array_second)
    final_image = Image.fromarray(np.uint8(final_array))

    return final_image


def process_operation(
        command: str,
        rgb_message: str,
        path_first: pathlib.Path,
        path_second: pathlib.Path,
        user_id: int,
) -> Optional[pathlib.Path]:
    """
    Call functions to perform mathematical operations on images.

    Args:
        command: Operation name.
        rgb_message: Channel that to work.
        path_first: Path for first image.
        path_second: Path for second image.
        user_id: User id that send message.

    Returns:
        Path for result image or None is something is wrong.
    """
    log.info('Start processing work with image')
    first_image: Image.Image = Image.open(path_first)
    second_image: Image.Image = Image.open(path_second)
    first_image, second_image = resize_pictures(first_image, second_image)

    if command == 'SUM':
        photo = summation(first_image, second_image, rgb_message)
    elif command == 'AVER':
        photo = average(first_image, second_image, rgb_message)
    elif command == 'MAX':
        photo = maximum(first_image, second_image, rgb_message)
    elif command == 'MIN':
        photo = minimum(first_image, second_image, rgb_message)
    elif command == 'CIRCLE MASK':
        photo = create_circle_mask(first_image)
    elif command == 'SQUARE MASK':
        photo = create_squared_mask(first_image)
    elif command == 'RECTANGLE MASK':
        photo = create_rectangle(first_image)
    else:
        log.warning('On known command!')
        return None

    path = path_first.parent / f'{user_id}_result.jpg'
    photo.save(path)
    log.info('Processed successful!')

    return path
