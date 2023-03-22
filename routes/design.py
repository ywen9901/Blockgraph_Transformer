from model.static import scripts, designdict, stackdict, curstack

from fastapi import APIRouter

router = APIRouter()

@router.post("/design/", tags=["design"])
def add_design(id=0):
    try:
        designdict[id] = {}
        stackdict[curstack].append(id)
    except Exception as error:
        repr(error)
        return -1

@router.delete("/design/", tags=["design"])
def del_design(stackid=0, designid=0):
    try:
        stackdict[stackid].remove(designid)
        designdict.pop(designid)
    except Exception as error:
        repr(error)
        return -1
