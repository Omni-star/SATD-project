# PyDriller use your local git credential
# to access on git platform and your own repositories,
# beyond all public repositories
import asyncio
import os

from datetime import datetime
from pydriller import Repository, Git

from unisannio.ingsoft.satd.git.analysis_status import AnalysisStatus
from unisannio.ingsoft.satd.webapp.data_manager import DataManager


class GitAnalyser:

  def __init__(self, repository_uri: str):
    self.repository_uri = repository_uri
    self.status = AnalysisStatus.NOT_STARTED

  def print_commits(self):
    repository = Repository(
      path_to_repo=self.repository_uri
    )

    try:
      for commit in repository.traverse_commits():
        print("{\"Commit\": {\"changedLines\": ", commit.lines,
              ", \"changedFiles\": \"", commit.files,
              ", \"id\": \"", commit.hash, "}}")
    except Exception as err:
      print(err, " - error while trying to access to repository commits.")

  def clone_repository(self, clone_path: str):
    os.makedirs(clone_path, exist_ok=True)

    repository: Repository = Repository(
      path_to_repo=self.repository_uri,
      clone_repo_to=clone_path
    )

    try:
      total_commit = 0
      for commit in repository.traverse_commits():
        print("{\"Commit\": {\"changedLines\": ", commit.lines,
              ", \"changedFiles\": \"", commit.files,
              ", \"id\": \"", commit.hash, "}}")
        total_commit += 1
      print("Total commit: " + str(total_commit))
    except Exception as err:
      print(err, " - error while trying to clone repository.")
      self._on_error()

  def get_file_list_to_analyse(self, clone_path: str, file_types: tuple[str]) -> [str]:
    file_to_analyse: list[str] = []
    self.status = AnalysisStatus.IN_PROGRESS

    self.clone_repository(clone_path=clone_path)
    if self.status == AnalysisStatus.ERROR:
      print("File to analyse finding Error")
      return

    repository_path = self.repository_uri.split("/")[-1]
    repository_path = clone_path + "/" + repository_path

    gr = Git(
      path=repository_path
    )
    for file_name in gr.files():
      for file_type in file_types:
        if file_name.endswith(file_type):
          file_to_analyse.append(file_name)
          break

    print("Numero file nel repository: ", len(gr.files()))
    print("Numero file da analizzare: ", len(file_to_analyse))

    return file_to_analyse

  def run_satd_analysis(self,
                        clone_path: str,
                        file_types: tuple[str, ...],
                        satd_keywords: tuple[str, ...],
                        output_path: str,
                        status_timeout_m: int = 3
                        ):
    file_to_analyse: list[str] = []
    repository_satd_keywords: list[str] = []
    self.status = AnalysisStatus.IN_PROGRESS

    self.clone_repository(clone_path=clone_path)
    if self.status == AnalysisStatus.ERROR:
      print("Analysis Error")
      return

    repository_name = self.repository_uri.split("/")[-1]
    repository_path = os.path.join(clone_path, repository_name)

    totalFilesAnalyzed: int = 0
    filesWithSATD: int = 0
    result: dict = {}
    print("Analyzing " + repository_path)
    for curDirPath, paths, filesName in os.walk(repository_path):
      print(paths)
      for file in filesName:
        print(file)
        if file.endswith(file_types):
          totalFilesAnalyzed += 1
          print(f"Total files Analyzed: {totalFilesAnalyzed}")

          satd: int = 0
          totalLines: int = 0
          lines: list[str] = []
          with open(os.path.join(curDirPath, file), 'r') as f:
            for i, line in enumerate(f):
              for keyword in satd_keywords:
                if keyword.lower() in line.lower():
                  # print(f"{file}:{i + 1}: {line.strip()}")
                  if not keyword in repository_satd_keywords:
                    repository_satd_keywords.append(keyword)

                  lines.append(f"{i + 1}: {line.strip()}")
                  satd += 1
                  break
              totalLines = i

            if satd > 0:
              filesWithSATD += 1

          print(f"\n{file} -> SATD lines: {satd}, total lines: {totalLines}\n\n")

          if not result.get(satd):
            result[satd]: list[any] = []

          # files_list: list[any] = []
          # for i in range(len(result.get(satd))):
          #   file_name: str = file.lower()
          #   if result[satd][i]['name'].lower() > file_name:
          #     files_list.append(
          #       {
          #         "name": file,
          #         "totalLines": totalLines,
          #         "SATDLines": lines
          #       }
          #     )
          #     for j in range(len(result.get(satd))):
          #       files_list.append(result.get(satd)[i])
          #
          #     break
          #   files_list.append(result.get(satd)[i])
          #
          # if len(files_list) == len(result.get(satd)):
          #   files_list.append(
          #     {
          #       "name": file,
          #       "totalLines": totalLines,
          #       "SATDLines": lines
          #     }
          #   )
          #
          # result[satd] = files_list

          result[satd].append(
            {
              "name": file,
              "totalLines": totalLines,
              "SATDLines": lines
            }
          )

    current_timestamp = int(datetime.now().timestamp())
    self._save_repository({
      "name": repository_name,
      "totalFiles": totalFilesAnalyzed,
      "filesWithSATD": filesWithSATD,
      "SATDWords": repository_satd_keywords,
      "creationDate": current_timestamp
    }, output_path, "repositories.json")

    DataManager.save_data(
      os.path.join(output_path, repository_name),
      f"{repository_name}:{current_timestamp}.json",
      result
    )

    self._on_done()

    return asyncio.run(self._reset_status(status_timeout_m))

  def _save_repository(self, repository: dict, output_path: str, file_name: str) -> bool:
    repositories_list: list[dict] = DataManager.load_data(os.path.join(output_path, file_name))
    ordered_rep_list: list[dict] = []
    if not repository.get('creationDate'):
      repository['creationDate'] = int(datetime.now().timestamp())

    if repositories_list:
      for i in range(len(repositories_list)):
        repository_name: str = repository['name'].lower()
        if repositories_list[i]['name'].lower() > repository_name:
          ordered_rep_list.append(repository)
          for j in range(i, len(repositories_list)):
            ordered_rep_list.append(repositories_list[j])

          break

        ordered_rep_list.append(repositories_list[i])
    else:
      ordered_rep_list = [repository]
      return DataManager.save_data(output_path, file_name, ordered_rep_list)

    if len(ordered_rep_list) == len(repositories_list):
      ordered_rep_list.append(repository)

    return DataManager.save_data(output_path, file_name, ordered_rep_list)

  def get_analysis_status(self) -> AnalysisStatus:
    return self.status

  def _on_error(self):
    print("ERRORE: ")
    self.status = AnalysisStatus.ERROR

  def _on_done(self):
    self.status = AnalysisStatus.DONE

  async def _reset_status(self, action_delay: int = 3):

    await asyncio.sleep(action_delay*60)

    self.status = AnalysisStatus.NOT_STARTED
