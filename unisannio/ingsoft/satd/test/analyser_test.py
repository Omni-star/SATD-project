import os.path

from unisannio.ingsoft.satd.git.git_analyser import GitAnalyser


def test_print_commits():
  git_analyser = GitAnalyser("https://github.com/openfga/openfga")
  git_analyser.print_commits()


def test_clone_repository():
  git_analyser = GitAnalyser("https://github.com/openfga/openfga")
  print(os.getcwd())
  clone_directory = "../../../../resources/repos"
  cloned_repository_path = os.path.join(clone_directory, "openfga")

  git_analyser.clone_repository(clone_directory)

  assert os.path.exists(cloned_repository_path)

  git_analyser.delete_local_repository(cloned_repository_path)

  assert not os.path.exists(cloned_repository_path)
