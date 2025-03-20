from enum import Enum


class UpdateEventResponseChangeAttachment(str, Enum):
    ADDREMOVE = "addRemove"
    NOCHANGE = "noChange"
    OWERWRITE = "owerwrite"

    def __str__(self) -> str:
        return str(self.value)
