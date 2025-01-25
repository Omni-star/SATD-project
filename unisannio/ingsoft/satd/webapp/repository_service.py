import asyncio
import os.path
from math import ceil

from unisannio.ingsoft.satd.git.analysis_status import AnalysisStatus
from unisannio.ingsoft.satd.git.git_analyser import GitAnalyser
from unisannio.ingsoft.satd.webapp.data_manager import DataManager
from datetime import datetime


class RepositoryService:
  def __init__(self, data_directory: str = "resources/data"):
    self.json_file_path = os.path.join(data_directory, 'repositories.json')
    self.git_analyser = GitAnalyser("https://github.com/Omni-star/SATD-project")

  def get_paged_repositories(self, page_index: int = 0, page_size: int = 0, filter: str = "", order: str = "ASC") -> \
      any:
    repositories_list: list[any] = DataManager.load_data(self.json_file_path)

    filter = filter.strip()
    if filter:
      filtered_repository: list[any] = []
      filter = filter.lower()

      for repository in repositories_list:
        if filter in str(repository['name']).lower():
          filtered_repository.append(repository)
          print("filtrando")

      repositories_list = filtered_repository

    total_repository: int = len(repositories_list)
    total_pages: int = ceil(total_repository/page_size)
    if page_size > 0:
      start_index: int = page_index * page_size
      if start_index >= total_repository:
          return {
            "pageIndex": page_index,
            "totalPages": total_pages,
            "content": []
          }

      end_index: int = start_index + page_size

      repositories_list = repositories_list[start_index:end_index]

    return {
      "pageIndex": page_index,
      "totalPages": total_pages,
      "content": repositories_list
    }

  def get_repositories(self) -> list[any]:
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

  async def start_repository_analysis(self,
                         repository_uri: str,
                         clone_repos_directory: str,
                         file_type_to_analyse: [str],
                         satd_keywords: [str],
                         data_directory: str
                         ) -> bool:
    self.git_analyser = GitAnalyser(repository_uri)

    self.git_analyser.run_satd_analysis(
      clone_repos_directory,
      file_type_to_analyse,
      satd_keywords,
      data_directory
    )

  def get_analysis_status(self) -> AnalysisStatus:
    return self.git_analyser.get_analysis_status()
