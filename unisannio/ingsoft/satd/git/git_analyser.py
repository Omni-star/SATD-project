# PyDriller use your local git credential
# to access on git platform and your own repositories,
# beyond all public repositories
import os

from datetime import datetime
from pydriller import Repository, Git

from unisannio.ingsoft.satd.webapp.data_manager import DataManager


class GitAnalyser:

  def __init__(self, repository_uri: str):
    self.repository_uri = repository_uri

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
    repository: Repository = Repository(
      path_to_repo=self.repository_uri,
      clone_repo_to=clone_path
    )

    try:
      for commit in repository.traverse_commits():
        commit
    except Exception as err:
      print(err, " - error while trying to clone repository.")

  def _get_file_list_to_analyse(self, clone_path: str, file_types: tuple[str]) -> [str]:
    file_to_analyse: [str] = []

    self.clone_repository(clone_path=clone_path)

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
    print("Numero file da analizzare: ", len(file_to_analyse.count()))

    return file_to_analyse

  def run_satd_analysis(self, clone_path: str, file_types: tuple[str, ...], satd_keywords: tuple[str, ...], output_path: str):
    file_to_analyse: list[str] = []

    self.clone_repository(clone_path=clone_path)

    repository_name = self.repository_uri.split("/")[-1]
    repository_path = os.path.join(clone_path, repository_name)

    totalFilesAnalyzed: int = 0
    filesWithSATD: int = 0
    result: list[dict] = []
    for curDirPath, _, filesName in os.walk(repository_path):
      for file in filesName:
        if file.endswith(file_types):
          totalFilesAnalyzed += 1

          satd: int = 0
          totalLines: int = 0
          lines: list[str] = []
          with open(os.path.join(curDirPath, file), 'r') as f:
            for i, line in enumerate(f):
              if any(keyword in line for keyword in satd_keywords):
                #print(f"{file}:{i + 1}: {line.strip()}")
                lines.append(f"{i + 1}: {line.strip()}")
                satd += 1
              totalLines = i

            if satd > 0:
              filesWithSATD += 1

          print(f"\n{file} -> SATD lines: {satd}, total lines: {totalLines}\n\n")
          result.append(
            {
              "name": file,
              "SATDLines": satd,
              "totalLines": totalLines,
              "SATD": lines
            }
          )

    self.save_repository({
      "name": repository_name,
      "filesWithSATD": filesWithSATD,
      "totalFiles": totalFilesAnalyzed,
      "creationDate": datetime.now().strftime("%d %B %Y")
    }, output_path, "repositories.json")

    DataManager.save_data(os.path.join(output_path, repository_name), f"{repository_name}.json", result)

  def save_repository(self, repository: dict, output_path: str, file_name: str) -> bool:
    repositories_list: list[dict] = DataManager.load_data(os.path.join(output_path, file_name))
    ordered_rep_list: list[dict] = []
    repository['creationDate'] = datetime.now().strftime("%d %B %Y")

    for i in range(len(repositories_list)):
      repository_name: str = repository['name'].lower()
      if repositories_list[i]['name'].lower() > repository_name:
        ordered_rep_list.append(repository)
        for j in range(i, len(repositories_list)):
          ordered_rep_list.append(repositories_list[j])

        break

      ordered_rep_list.append(repositories_list[i])

    if len(ordered_rep_list) == len(repositories_list):
      ordered_rep_list.append(repository)

    return DataManager.save_data(output_path, file_name, ordered_rep_list)
