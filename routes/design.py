from model.static import History

from fastapi import APIRouter

router = APIRouter()

@router.post("/design", tags=["design"])
def add_design(history: History, id=0):
    try:
        history.designdict[id] = {}
        history.stackdict[history.curstack].append(id)
    except Exception as error:
        repr(error)
        return -1

@router.delete("/design/{designid}", tags=["design"])
def del_design(history: History, stackid=0, designid=0):
    try:
        history.stackdict[stackid].remove(designid)
        history.designdict.pop(designid)
    except Exception as error:
        repr(error)
        return -1
