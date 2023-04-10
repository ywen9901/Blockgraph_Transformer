from app.internal.initialization import get_new_stackid

from app.model.static import History

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/history/", tags=["history"])
def add_stack(history: History, id=0):
    try:
        newid = get_new_stackid('stack')
    except:
        raise HTTPException(status_code=500, detail="Failed to create new stack ID")
    
    history.stackdict[newid] = []
    history.stackdict[newid].append(history.stackloc[history.curstack])
    history.stackloc[newid] = history.stackloc[history.curstack]
    history.curstack = newid

    return history

@router.delete("/history/", tags=["history"])
def del_stack(history: History, stackid):
    if stackid not in history.stackdict:
        raise HTTPException(status_code=404, detail="Stack ID not found")
    
    # delete all designs in this stack (execpt stack[0])
    for design in history.stackdict[stackid][1:]:
        del history.designdict[design]

    # update stack pointer if needed
    if history.curstack == stackid:
        stacklist = list(history.stackdict.keys())
        if stacklist.index(history.curstack) - 1 < 0:
            history.curstack = stacklist[stacklist.index(history.curstack) + 1]
        else:
            history.curstack = stacklist[stacklist.index(history.curstack) - 1]
    
    del history.stackdict[stackid]
    del history.stackloc[stackid]

    return history

@router.put("/history/{stackid}", tags=["history"])
def swt_stack(history: History, stackid):
    try:
        history.stackdict[stackid]
        history.curstack = stackid
    except:
        raise HTTPException(status_code=404, detail="Stack ID not found")
