import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pathlib
import logging
from typing import Optional


log = logging.getLogger(__name__)


def plot_darker() -> None:
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = (first_array * first_array) // 255
    plt.plot(first_array, second_array, '-')


def plot_lighter() -> None:
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = np.sqrt(first_array * 255)
    plt.plot(first_array, second_array, '-')
    plt.axis([-2, 255, -2, 255])


def plot_negative() -> None:
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = first_array * (-1) + 255
    plt.plot(first_array, second_array, '-')
    plt.axis([-2, 255, -2, 255])


def plot_sigmoid() -> None:
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = 255 / (1 + np.exp(-(first_array - 128)))
    plt.plot(first_array, second_array, '-')


def plot_function(
        message: str,
        user_id: int,
        data_path: pathlib.Path,
) -> Optional[pathlib.Path]:
    """Plot gradation transformation function.

    Args:
        message: Contains the name of gradation transformation function.
        user_id: User id that send message.
        data_path: Path where save images.

    Returns:
        Path where saved final image or None if something is wrong.
    """
    log.info('Start plot gradation transformation plot')
    if message == 'darker':
        plot_darker()
    elif message == 'lighter':
        plot_lighter()
    elif message == 'negative':
        plot_negative()
    elif message == 'sigmoid':
        plot_sigmoid()
    else:
        return None

    log.info('Plotting completed successfully!')

    final_path = data_path / f'{user_id}_second_lab_2_operation.jpg'
    plt.savefig(final_path)
    plt.clf()
    return final_path


def darker(image: Image.Image) -> Image.Image:
    array = np.asarray(image)
    array = np.uint16(array)
    step_one = array * array
    step_two = step_one // 255
    np.putmask(step_two, step_two > 255, 255)
    new_image = Image.fromarray(np.uint8(step_two))

    return new_image


def negative(image: Image.Image) -> Image.Image:
    array = np.asarray(image)
    array = np.uint16(array)
    step_two = array * (-1) + 255
    np.putmask(step_two, step_two > 255, 255)
    new_image = Image.fromarray(np.uint8(step_two))

    return new_image


def sigmoid(image: Image.Image) -> Image.Image:
    array = np.asarray(image)
    array = np.int64(array)
    step_one = 255 / (1 + np.exp(-(array - 128)))
    np.putmask(step_one, step_one > 255, 255)
    new_image = Image.fromarray(np.uint8(step_one))

    return new_image


def lighter(image: Image.Image) -> Image.Image:
    array = np.asarray(image)
    array = np.uint16(array)
    first_step = array * 255
    second_step = np.sqrt(first_step)
    np.putmask(second_step, second_step > 255, 255)
    new_image = Image.fromarray(np.uint8(second_step))

    return new_image


def operations(
        message: str,
        path: pathlib.Path,
        user_id: int
) -> Optional[pathlib.Path]:
    """Process start to create new image using gradation transformations.

    Args:
        message: Contains the name of gradation transformation.
        path: Contains the path where saved image.
        user_id: User id that send message.

    Returns:
        Path for new image or None if something is wrong.
    """
    log.info('Start processing gradation transformation on image')
    image = Image.open(path)
    if message == 'darker':
        photo = darker(image)
    elif message == 'negative':
        photo = negative(image)
    elif message == 'sigmoid':
        photo = sigmoid(image)
    elif message == 'lighter':
        photo = lighter(image)
    else:
        return None

    log.info('Gradation transformation was successful!')

    picture_path = path.parent / f'{user_id}_final_lab_2_image.jpg'
    photo.save(picture_path)
    return picture_path
