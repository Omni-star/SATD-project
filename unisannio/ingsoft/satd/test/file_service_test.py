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
test_files_open_repository = {
  "1": [
    {
      "name": "flags.go",
      "totalLines": 291,
      "SATDLines": [
        "212: // TODO: make breaking change for cache limit"
      ]
    }
  ],
  "3": [
    {
      "name": "storage.go",
      "totalLines": 347,
      "SATDLines": [
        "282: // CreateStore must return an error if the store ID or the name aren't set. TODO write test.",
        "287: // If the store ID didn't exist it must return ErrNotFound. TODO write test (memory doesn't satisfy this?)",
        "293: // ListStores returns a list of non-deleted stores that match the provided options. TODO write test with the IDs filter."
      ]
    }
  ]
}


def setup_module(module):
  print("setup")
  DataManager.save_data(os.path.join(data_directory, "openTest"), "openTest:237139127.json", test_files_open_test)
  DataManager.save_data(os.path.join(data_directory, "openRepository"), "openRepository:237139127.json",
                        test_files_open_repository)


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
