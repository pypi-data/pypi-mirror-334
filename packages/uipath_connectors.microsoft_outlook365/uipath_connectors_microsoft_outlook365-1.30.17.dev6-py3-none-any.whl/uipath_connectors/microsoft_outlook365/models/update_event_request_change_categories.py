from enum import Enum


class UpdateEventRequestChangeCategories(str, Enum):
    ADDREMOVE = "addRemove"
    NOCHANGE = "noChange"
    OVERWRITE = "overwrite"

    def __str__(self) -> str:
        return str(self.value)
