import json
from typing import Union, Any


class DataManager:

  @staticmethod
  def load_data(json_file_path: str) -> Union[Any, None]:
    data: Any = None
    try:
      with open(json_file_path) as f:
        data = json.load(f)
    except FileNotFoundError as e:
      return None
    return data

  @staticmethod
  def save_data(json_file_path: str, data: Any) -> bool:
    try:
      with open(json_file_path, "w") as f:
        json.dump(data, f, indent=2)
    except FileNotFoundError as e:
      return False
    return True
