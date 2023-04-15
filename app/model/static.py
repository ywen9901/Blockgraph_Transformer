# Global var for apis

from .example import infodict
from pydantic import BaseModel
from typing import Union
class Design(BaseModel):
    blockdict: dict = {}
    linkdict: dict = {}
    containerdict: dict = {}
    groupdict: dict = {}
    templatedict: dict = {}
    labeldict: dict = {}

    class Config:
        orm_mode = True

class Connection(BaseModel):
    block: str
    link: str

class History(BaseModel):
    stackdict: dict = {}
    designdict: dict = {}
    curstack: str = ""
    stackloc: dict = {}

    class Config:
        orm_mode = True

global tfidx
tfidx = {'block': 8, 'port': 9, 'link': 5, 'slot': 13, 'group': 0}

global stackidx, designdict, stackdict, curstack, stackloc
stackidx = {'stack': 1, 'design': 1}
designdict = {'D0': infodict['design']}
stackdict = {'S0': ['D0']}
curstack = 'S0'
stackloc = {'S0': 'D0'}