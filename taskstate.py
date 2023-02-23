import json
from enum import Enum

class TaskState(Enum):
    QUEUED = 0
    DOWNLOADING = 15
    DOWNLOADED = 30
    SEPARATING = 45
    SEPARATED = 60
    TRANSCRIBING = 75
    TRANSCRIBED = 90
    FINISHED = 100
    ERROR = -1

    def __json__(self):
        return f"__enum__TaskState.{self.name}"

    def fromJSON(json_str):
        if '__enum__' in json_str:
            if json_str[18:] == 'QUEUED':
                return TaskState.QUEUED
            elif json_str[18:] == 'DOWNLOADING':
                return TaskState.DOWNLOADING
            elif json_str[18:] == 'DOWNLOADED':
                return TaskState.SEPARATING
            elif json_str[18:] == 'SEPARATING':
                return TaskState.SEPARATED
            elif json_str[18:] == 'SEPARATED':
                return TaskState.DOWNLOADING
            elif json_str[18:] == 'TRANSCRIBING':
                return TaskState.TRANSCRIBING
            elif json_str[18:] == 'TRANSCRIBED':
                return TaskState.TRANSCRIBED
            elif json_str[18:] == 'FINISHED':
                return TaskState.FINISHED
            else:
                return TaskState.ERROR