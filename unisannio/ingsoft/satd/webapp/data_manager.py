import json
import os
import shutil
import sys
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
  def save_file_data(json_file_path: str, data: Any) -> bool:
    try:
      if not os.path.exists(json_file_path):
        file_name = json_file_path.split("/")[-1]
        new_directory = json_file_path.replace(file_name, "")
        os.makedirs(new_directory, exist_ok=True)
      with open(json_file_path, "w") as f:
        json.dump(data, f, indent=2)
    except FileNotFoundError as e:
      return False
    return True

  @staticmethod
  def save_data(json_file_path: str, file_name: str, data: Any) -> bool:
    try:
      os.makedirs(json_file_path, exist_ok=True)
      with open(os.path.join(json_file_path, file_name), "w") as f:
        json.dump(data, f, indent=2)
    except FileNotFoundError as e:
      return False
    return True

  @staticmethod
  def delete_local_repository(repository_path: str):
    try:
      shutil.rmtree(repository_path)
      print(f"The folder '{repository_path}' has been removed successfully.")
    except OSError as e:
      print(f"Error while removing the folder: {e}", file=sys.stderr)
