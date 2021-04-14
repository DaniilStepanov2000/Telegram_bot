import pathlib
import json
from dataclasses import dataclass


@dataclass
class Settings:
    """Class for storing settings.

    Args:
        telegram_bot_token: Token for telegram bot API.
        project_static_path: Path to static files.
    """
    telegram_bot_token: str
    project_static_path: pathlib.Path

    @classmethod
    def from_json(cls, file_path: pathlib.Path):
        with file_path.open('r') as file:
            our_config = json.load(file)

        return cls(
            telegram_bot_token=our_config.get('telegram_bot_token', ''),
            project_static_path=pathlib.Path(our_config.get('project_static_path', './data')),
        )
