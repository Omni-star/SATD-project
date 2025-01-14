# PyDriller use your local git credential
# to access on git platform and your own repositories,
# beyond all public repositories
import os

from pydriller import Repository, Git


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

  def run_satd_analysis(self, clone_path: str, file_types: tuple[str, ...], satd_keywords: tuple[str, ...]):
    file_to_analyse: list[str] = []

    self.clone_repository(clone_path=clone_path)

    repository_path = self.repository_uri.split("/")[-1]
    repository_path = clone_path + "/" + repository_path

    for curDirPath, _, filesName in os.walk(repository_path):
      for file in filesName:
        if file.endswith(file_types):
          satd: int = 0
          with open(os.path.join(curDirPath, file), 'r') as f:
            for i, line in enumerate(f):
              if any(keyword in line for keyword in satd_keywords):
                print(f"{file}:{i + 1}: {line.strip()}")
                satd += 1

          print(f"\n{file}:SATD: {satd}\n")
