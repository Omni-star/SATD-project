# This ingsoft a sample Python script.
import os
import shutil

from unisannio.ingsoft.satd.git.git_analyser import GitAnalyser
from unisannio.ingsoft.satd.configuration.config_manger import ConfigManager
from unisannio.ingsoft.satd.webapp.flask_app import SatdApp


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def _test_git_analyser():
  # Important it is to check the current directory
  print(os.getcwd())

  config = ConfigManager.load_configuration("resources/config/config.json")

  # Repository url and directory where clone repository into
  r_url: str = config["repository_url"]
  clone_to: str = config["clone_repos_directory"]
  data_directory: str = config["data_directory"]
  file_type_to_analyse: tuple[str] = tuple(config["file_type_to_analyse"])
  satd_keywords: tuple[str] = tuple(config["satd_keywords"])

  # Class to manage git repository and file analysis
  git_analyser = GitAnalyser(
    repository_uri=r_url
  )
  print(clone_to)

  # file_to_analyse: [str] = git_analyser.get_file_list_to_analyse(clone_to, "java", "go")
  git_analyser.run_satd_analysis(clone_to, file_type_to_analyse, satd_keywords, data_directory)

def _test_delete_local_repository():
  # Important it is to check the current directory
  print(os.getcwd())

  config = ConfigManager.load_configuration("resources/config/config.json")

  repository_name: str = 'clone_test_repo'
  clone_to: str = config["clone_repos_directory"]

  # Class to manage git repository and file analysis
  git_analyser = GitAnalyser(
    repository_uri='https://github.com/Omni-star/SATD-project'
  )
  print(clone_to)

  _prepare_directory()
  git_analyser.delete_local_repository(os.path.join(clone_to, repository_name))


def _test_web_app():
  config = ConfigManager.load_configuration("resources/config/config.json")

  # print(config["webapp_res_directory"])

  web_app = SatdApp(config)
  web_app.run()

def _prepare_directory():
  config = ConfigManager.load_configuration("resources/config/config.json")

  repository_name: str = 'test_repo'
  clone_repository_name: str = 'clone_test_repo'
  clone_to: str = config["clone_repos_directory"]

  try:
    shutil.copytree(os.path.join(clone_to, repository_name), os.path.join(clone_to, clone_repository_name))
    print(f"The '{os.path.join(clone_to, repository_name)}' directory has been copied in '{os.path.join(clone_to, clone_repository_name)}'.")
  except FileExistsError:
    print("Target directory already exists.")
  except OSError as e:
    print(f"Error while copying: {e}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  # _test_git_analyser()
  #_prepare_directory()
  #_test_delete_local_repository()
  _test_web_app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
