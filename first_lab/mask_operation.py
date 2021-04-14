from PIL import Image, ImageDraw
import numpy as np
from typing import List


def create_mask(width: int, height: int) -> Image.Image:
    """Create a mask.

    Args:
        width: Image width.
        height: Image height.

    Returns:
        One image that a mask.
    """
    width = width
    height = height

    mask = Image.new('RGB', (width, height))
    return mask


def width_height_circle_square(width: int, height: int) -> List[int]:
    width_square_first = (width - width // 2) - 20
    height_square_first = (height - height // 2) - 20

    width_square_second = (width - width // 2) + 20
    height_square_second = (height - height // 2) + 20

    return [width_square_first, height_square_first, width_square_second, height_square_second]


def perform_operation_on_mask(image: Image.Image, mask: Image.Image) -> Image.Image:
    """
    Applying a mask to an image.

    Args:
         image: The image that the mask will apply to.
         mask: Mask for overlaying an image.

    Returns:
        One image after applying the mask to it.
    """
    first_array = np.asarray(image, dtype=np.uint16)
    second_array = np.asarray(mask, dtype=np.uint16)

    final_array = first_array * second_array
    np.putmask(final_array, final_array > 255, 255)
    new_image = Image.fromarray(np.uint8(final_array))
    return new_image


def create_circle_mask(first_image: Image.Image) -> Image.Image:
    """Create a circle mask.

    Args:
        first_image: Default black image.

    Returns:
        One image that is circle mask.
    """
    width, height = first_image.size
    circle_mask = create_mask(width, height)

    draw = ImageDraw.Draw(circle_mask)

    width_height = width_height_circle_square(width, height)

    draw.ellipse(width_height, (1, 1, 1))

    new_image = perform_operation_on_mask(first_image, circle_mask)

    return new_image


def create_squared_mask(first_image: Image.Image) -> Image.Image:
    """Create a squared mask.

    Args:
         first_image: Default black image.

    Returns:
            One image that is squared mask.
    """
    width, height = first_image.size

    square_mask = create_mask(width, height)

    draw = ImageDraw.Draw(square_mask)

    width_height = width_height_circle_square(width, height)

    draw.rectangle(width_height, (1, 1, 1))

    new_image = perform_operation_on_mask(first_image, square_mask)

    return new_image


def width_height_rectangle(width: int, height: int) -> List[int]:
    width_rect_first = (width - width // 2) - 20
    height_rect_first = (height - height // 2) - 40

    width_rect_second = (width - width // 2) + 20
    height_rect_second = (height - height // 2) + 40

    return [width_rect_first, height_rect_first, width_rect_second, height_rect_second]


def create_rectangle(first_image: Image.Image) -> Image.Image:
    """Create a rectangle mask.

    Args:
        first_image: Default black image.

    Returns:
        One image that is rectangle mask.
    """
    width, height = first_image.size

    rectangle_mask = create_mask(width, height)

    draw = ImageDraw.Draw(rectangle_mask)

    width_height = width_height_rectangle(width, height)

    draw.rectangle(width_height, (1, 1, 1))

    new_image = perform_operation_on_mask(first_image, rectangle_mask)

    return new_image
