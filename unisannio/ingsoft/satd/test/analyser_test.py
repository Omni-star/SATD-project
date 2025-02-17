import os.path
import sys

from unisannio.ingsoft.satd.git.git_analyser import GitAnalyser
from unisannio.ingsoft.satd.webapp.data_manager import DataManager

repository_uri = "https://github.com/openfga/openfga"
repository_name = repository_uri.split("/")[-1]
file_types = ("go",)
satd_words = ("TODO", "FIXME", "Hack", "XXX")
test_directory = "../../../../resources/test"

#def setup_module(module):
#  print("Setup")  # Codice eseguito prima del test
#  DataManager.delete_local_repository(test_directory)

def teardown_function(function):
  print("Teardown")  # Codice eseguito dopo il test
  DataManager.delete_local_repository(test_directory)


def test_print_commits():
  git_analyser = GitAnalyser(repository_uri)
  git_analyser.print_commits()


def test_clone_repository():
  git_analyser = GitAnalyser(repository_uri)
  clone_directory = os.path.join(test_directory, "repos")
  cloned_repository_path = os.path.join(clone_directory, repository_name)

  assert not os.path.exists(cloned_repository_path)

  git_analyser.clone_repository(clone_directory)

  assert os.path.exists(cloned_repository_path)


def test_get_file_to_analyse():
  git_analyser = GitAnalyser(repository_uri)
  clone_directory = os.path.join(test_directory, "repos")
  cloned_repository_path = os.path.join(clone_directory, repository_name)

  assert not os.path.exists(cloned_repository_path)

  git_analyser.get_file_list_to_analyse(clone_directory, file_types)

  assert os.path.exists(cloned_repository_path)


def test_run_satd_analysis():
  git_analyser = GitAnalyser(repository_uri)
  clone_directory = os.path.join(test_directory, "repos")
  data_directory = os.path.join(test_directory, "data")
  cloned_repository_path = os.path.join(clone_directory, repository_name)

  assert not os.path.exists(cloned_repository_path)

  git_analyser.run_satd_analysis(
    clone_directory,
    file_types,
    satd_words,
    data_directory,
    0
  )

  assert os.path.exists(cloned_repository_path)
