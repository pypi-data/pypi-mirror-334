from enum import Enum


class UpdateEventResponseShowAs(str, Enum):
    BUSY = "busy"
    FREE = "free"
    OOF = "oof"
    TENTATIVE = "tentative"
    WORKINGELSEWHERE = "workingElsewhere"

    def __str__(self) -> str:
        return str(self.value)
