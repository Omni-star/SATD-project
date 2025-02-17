import os.path

from unisannio.ingsoft.satd.webapp.data_manager import DataManager
from unisannio.ingsoft.satd.webapp.repository_service import RepositoryService

test_directory = "../../../../resources/test"
data_directory = os.path.join(test_directory, "data")
data_file_name = "repositories.json"
test_repositories = [
  {
    "name": "openTest",
    "totalFiles": 277,
    "filesWithSATD": 23,
    "SATDWords": ["fixme", "todo"],
    "creationDate": 1738103796,
  },
  {
    "name": "openRepository",
    "totalFiles": 398,
    "filesWithSATD": 65,
    "SATDWords": ["hack"],
    "creationDate": 1733203796,
  },
  {
    "name": "openCode",
    "totalFiles": 1200,
    "filesWithSATD": 230,
    "SATDWords": ["xxx, todo"],
    "creationDate": 1738163796,
  }
]


def setup_module(module):
  print("setup")
  DataManager.save_data(
    data_directory,
    data_file_name,
    test_repositories
  )

def teardown_module(module):
  print("teardown")
  DataManager.delete_local_repository(test_directory)


def test_get_repositories():
  repository_service = RepositoryService(
    data_directory
  )
  repositories = repository_service.get_repositories()

  ok = False

  assert all(any(rep["name"] in repository["name"] for rep in test_repositories) for repository in repositories)


def test_get_all_paged_repositories():
  repository_service = RepositoryService(
    data_directory
  )
  repositories = repository_service.get_paged_repositories(
    page_index=0,
    page_size=1,
    filter="fix",
    order="ASC"
  )["content"]

  print(repositories)

  assert all(any(rep["name"] in repository["name"] for rep in test_repositories) for repository in repositories)


def test_get_paged_repositories():
  repository_service = RepositoryService(
    data_directory
  )
  repositories = repository_service.get_paged_repositories(
    page_index=0,
    page_size=1,
    filter="fix",
    order="ASC"
  )["content"]

  print(repositories)

  assert len(repositories) == 1


def test_get_paged_filtered_repositories():
  repository_service = RepositoryService(
    data_directory
  )
  repositories = repository_service.get_paged_repositories(
    page_index=0,
    page_size=100,
    filter="fix",
    order="ASC"
  )["content"]

  print(repositories)

  assert repositories[0]["name"] in test_repositories[0]["name"]