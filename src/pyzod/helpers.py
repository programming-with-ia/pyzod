from enum import Enum
from dataclasses import dataclass
import typing as t

T = t.TypeVar("T")


class CustomDict(dict):

    def setValue(self, key, value):
        # if value is None:
        #     del self[key]
        #     return
        self[key] = value

    def getValue(self, key):
        return self.get(key, None)


@dataclass
class ValidateResponse(t.Generic[T]):
    success: bool | t.Literal["warning"]
    error: t.Optional[Exception] = None
    data: t.Optional[T] = None


class MessagesTypes(Enum):
    Required = 0


def getUniqueObjects(objList: list | tuple):
    seenTypes = set()

    uniqueObjects = []

    for obj in objList:
        if type(obj) not in seenTypes:
            uniqueObjects.append(obj)
            seenTypes.add(type(obj))

    return type(objList)(uniqueObjects)


def getCN(obj):
    return obj.__class__.__name__
