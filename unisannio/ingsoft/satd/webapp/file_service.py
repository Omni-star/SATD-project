import os.path
from math import ceil

from unisannio.ingsoft.satd.webapp.data_manager import DataManager

class FileService:
  def __init__(self, data_directory: str = "resources/data"):
    self.data_directory = data_directory

  def get_folders(self,
                  repository_name: str,
                  page_index: int = 0,
                  page_size: int = 0,
                  order: str = "DESC"
                  ) -> any:
    folder_dict: dict[any] = DataManager.load_data(os.path.join(
      self.data_directory,
      repository_name.split(":")[0],
      f"{repository_name}.json")
    )

    total_repository: int = len(folder_dict)
    total_pages: int = ceil(total_repository / page_size)
    start_index: int = 0
    end_index: int = len(folder_dict.keys())
    if page_size > 0:
      start_index: int = page_index * page_size
      if start_index >= total_repository:
        return {
          "pageIndex": page_index,
          "totalPages": total_pages,
          "content": []
        }

      end_index: int = start_index + page_size

    folder_list: list[any] = []
    keys: list[int] = list(folder_dict.keys())
    if order == 'DESC':
      keys.sort(key=lambda k: int(k), reverse=True)
    else:
      keys.sort(key=lambda k: int(k))
    for key in keys[start_index:end_index]:
      folder_list.append({
        "satdNumber": key,
        "files": len(folder_dict[key])
      })

    return {
      "pageIndex": page_index,
      "totalPages": total_pages,
      "content": folder_list
    }

  def get_files(self,
                repository_name: str,
                satd_number: int,
                page_index: int = 0,
                page_size: int = 0,
                filter: str = "",
                order: str = "ASC"
                ) -> any:
    folder_dict: dict[any] = DataManager.load_data(os.path.join(
      self.data_directory,
      repository_name.split("-")[0],
      f"{repository_name}.json")
    )
    files_list: list[any] = folder_dict[satd_number]

    filter = filter.strip()
    if filter:
      filtered_files: list[any] = []
      filter = filter.lower()

      for file in files_list:
        if filter in str(file['name']).lower():
          filtered_files.append(file)
          print("filtrando")

      files_list = filtered_files

    total_files: int = len(files_list)
    total_pages: int = ceil(total_files / page_size)
    if page_size > 0:
      start_index: int = page_index * page_size
      if start_index >= total_files:
        return {
          "pageIndex": page_index,
          "totalPages": total_pages,
          "content": []
        }

      end_index: int = start_index + page_size

      if order == 'DESC':
        files_list.sort(key=lambda x: x['name'].lower(), reverse=True)
      else:
        files_list.sort(key=lambda x: x['name'].lower())

      files_list = files_list[start_index:end_index]

    return {
      "pageIndex": page_index,
      "totalPages": total_pages,
      "content": files_list
    }