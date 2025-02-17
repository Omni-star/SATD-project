import os

from unisannio.ingsoft.satd.webapp.data_manager import DataManager
from unisannio.ingsoft.satd.webapp.file_service import FileService

test_directory = "../../../../resources/test"
data_directory = os.path.join(test_directory, "data")
test_files_open_test = {
  "0": [
    {
      "name": "version.go",
      "totalLines": 27,
      "SATDLines": []
    },
  ],
  "1": [
    {
      "name": "mysql.go",
      "totalLines": 820,
      "SATDLines": [
        "445: // TODO: make this concurrent with a maximum of 5 goroutines. This may be helpful:"
      ]
    },
    {
      "name": "resolver.go",
      "totalLines": 104,
      "SATDLines": [
        "19: // FIXME: there is a duplicate cache of models elsewhere: https://github.com/opentest/opentest/issues/1045"
      ]
    }
  ]
}


def setup_function(function):
  print("setup")
  DataManager.save_data(os.path.join(data_directory, "openTest"), "openTest:237139127.json", test_files_open_test)


def teardown_function(function):
  print("teardown")
  DataManager.delete_local_repository(test_directory)

def test_get_folders():
  file_service = FileService(data_directory)
  folders = file_service.get_folders(
    repository_name="openTest:237139127",
    page_index=0,
    page_size=100,
    order="DESC"
  )["content"]

  assert folders

  print(folders)

  ok = False
  if all(len(test_files_open_test[folder["satdNumber"]]) == folder["files"] for folder in folders):
    ok = True

  assert ok


def test_get_files():
  file_service = FileService(data_directory)
  files = file_service.get_files(
    repository_name="openTest:237139127",
    satd_number="1",
    page_index=0,
    page_size=100,
    filter="",
    order="ASC"
  )["content"]

  assert files

  print(files)

  assert len(files) == len(test_files_open_test["1"])


def test_get_filtered_files():
  file_service = FileService(data_directory)
  files = file_service.get_files(
    repository_name="openTest:237139127",
    satd_number="1",
    page_index=0,
    page_size=100,
    filter="todo",
    order="ASC"
  )["content"]

  assert files

  print(files)

  assert len(files) == 1
