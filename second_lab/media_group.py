from typing import Tuple

from aiogram import types


def create_media(paths: Tuple[str, str, str, str]) -> types.MediaGroup:
    media = types.MediaGroup()

    media.attach_photo(types.InputFile(paths[3]), caption='Average histogram')
    media.attach_photo(types.InputFile(paths[0]), caption='R channel histogram')
    media.attach_photo(types.InputFile(paths[1]), caption='B channel histogram')
    media.attach_photo(types.InputFile(paths[2]), caption='G channel  histogram')
    return media
