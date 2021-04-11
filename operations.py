from typing import List, Tuple
from rgb_channel import channel_function

import numpy as np
from PIL import Image
from aiogram.types import PhotoSize

from mask_operation import create_circle_mask, create_squared_mask, create_rectangle


def get_max_sized_photo(photos: List[PhotoSize]) -> PhotoSize:
    max_photo = photos[0]
    for photo in photos[1:]:
        if photo.width > max_photo.width:
            max_photo = photo

    return max_photo


def resize_pictures(first_image: Image.Image, second_image: Image.Image) -> Tuple[Image.Image, Image.Image]:
    first_size = first_image.size
    print(first_size)
    second_size = second_image.size
    print(second_size)
    result = (tuple(zip(first_size, second_size)))

    width = max(result[0])
    height = max(result[1])

    print(tuple([width, height]))
    new_first_image = first_image.resize(tuple([width, height]))
    new_second_image = second_image.resize(tuple([width, height]))

    new_first_image.save(r'C:\Users\dan-s\PycharmProjects\bot\first_picture.jpg')
    new_second_image.save(r'C:\Users\dan-s\PycharmProjects\bot\second_picture.jpg')

    return new_first_image, new_second_image


def summation(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> str:
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.add(np.uint8(tuple_array_first), np.uint8(tuple_array_second), dtype=np.uint16)
    np.putmask(final_array, final_array > 255, 255)
    final_image = Image.fromarray(np.uint8(final_array))
    path_file = r'C:\Users\dan-s\PycharmProjects\bot\sum.jpg'
    final_image.save(path_file)

    return path_file


def average(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> str:
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.add(np.uint8(tuple_array_first), np.uint8(tuple_array_second), dtype=np.uint16) // 2
    np.putmask(final_array, final_array > 255, 255)
    final_image = Image.fromarray(np.uint8(final_array))
    path_file = r'C:\Users\dan-s\PycharmProjects\bot\aver.jpg'
    final_image.save(path_file)

    return path_file


def maximum(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> str:
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.maximum(tuple_array_first, tuple_array_second)
    final_image = Image.fromarray(np.uint8(final_array))
    path_file = r'C:\Users\dan-s\PycharmProjects\bot\max.jpg'
    final_image.save(path_file)

    return path_file


def minimum(first_image: Image.Image, second_image: Image.Image, rgb_message: str) -> str:
    tuple_array_first = np.asarray(first_image)
    tuple_array_second = np.asarray(second_image)
    tuple_array_second = channel_function(tuple_array_second, rgb_message)  # переделать channel_function

    final_array = np.minimum(tuple_array_first, tuple_array_second)
    final_image = Image.fromarray(np.uint8(final_array))
    path_file = r'C:\Users\dan-s\PycharmProjects\bot\min.jpg'
    final_image.save(path_file)

    return path_file


def get_way(command: str, rgb_message: str) -> str:
    first_image: Image.Image = Image.open(r'C:\Users\dan-s\PycharmProjects\bot\first_picture.jpg')
    second_image: Image.Image = Image.open(r'C:\Users\dan-s\PycharmProjects\bot\second_picture.jpg')
    first_image, second_image = resize_pictures(first_image, second_image)
    if command == 'SUM':
        return summation(first_image, second_image, rgb_message)
    if command == 'AVER':
        return average(first_image, second_image, rgb_message)
    if command == 'MAX':
        return maximum(first_image, second_image, rgb_message)
    if command == 'MIN':
        return minimum(first_image, second_image, rgb_message)
    if command == 'CIRCLE MASK':
        return create_circle_mask(first_image, second_image)
    if command == 'SQUARE MASK':
        return create_squared_mask(first_image, second_image)
    if command == 'RECTANGLE MASK':
        return create_rectangle(first_image, second_image)
