import json
from typing import Union, Any


class ConfigManager:

    @staticmethod
    def load_configuration(json_file_path: str) -> Union[Any, None]:
        config: Any = None
        with open(json_file_path) as f:
            config = json.load(f)
        return config