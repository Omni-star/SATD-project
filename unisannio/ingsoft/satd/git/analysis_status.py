from enum import Enum


class AnalysisStatus(Enum):
  NOT_STARTED = 0
  IN_PROGRESS = 1
  DONE = 2
  ERROR = 3

  def __str__(self):
    return self.name