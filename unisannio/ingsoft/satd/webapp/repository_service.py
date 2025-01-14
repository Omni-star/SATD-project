import os.path

from unisannio.ingsoft.satd.webapp.data_manager import DataManager
from datetime import datetime

class RepositoryService:
  def __init__(self, data_directory: str = "resources/data"):
    self.json_file_path = os.path.join(data_directory, 'repositories.json')

  def get_paged_repositories(self, page_index: int = 0, page_size: int = 0, filter: str = "", order: str = "ASC") -> \
    list[any]:
    repositories_list: list[any] = DataManager.load_data(self.json_file_path)

    if page_size > 0:
      start_index: int = page_index * page_size
      end_index: int = start_index + page_size
      repositories_list = repositories_list[start_index:end_index]

    filter = filter.strip()
    if filter:
      filter = filter.lower()
      filtered_repository: list[any] = []

      for repository in repositories_list:
        if filter in str(repository['name']).lower():
          filtered_repository.append(repository)

        return filtered_repository

    return repositories_list

  def get_repositories(self, page_index: int = 0, page_size: int = 0, filter: str = "") -> list[any]:
    repositories_list: list[any] = DataManager.load_data(self.json_file_path)

    return repositories_list

  def save_repository(self, repository: any) -> bool:
    repositories_list: list[any] = DataManager.load_data(self.json_file_path)
    ordered_rep_list: list[any] = []
    repository['creationDate'] = datetime.now().strftime("%d %B %Y")

    for i in range(len(repositories_list)):
      if repositories_list[i]['name'] > repository['name']:
        ordered_rep_list.append(repository)
        for j in range(i, len(repositories_list)):
          ordered_rep_list.append(repositories_list[j])

        break

      ordered_rep_list.append(repositories_list[i])

    if len(ordered_rep_list) == len(repositories_list):
      ordered_rep_list.append(repository)

    return DataManager.save_data(self.json_file_path, ordered_rep_list)
