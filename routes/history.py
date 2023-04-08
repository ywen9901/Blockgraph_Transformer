from internal.initialization import get_new_stackid

from model.static import History

from fastapi import APIRouter

router = APIRouter()

@router.post("/history/", tags=["history"])
def add_stack(history: History, id=0):
    newid = get_new_stackid('stack')
    history.stackdict[newid] = []
    history.stackdict[newid].append(history.stackloc[history.curstack])
    history.stackloc[newid] = history.stackloc[history.curstack]
    history.curstack = newid

@router.delete("/history/", tags=["history"])
def del_stack(history: History, stackid=0):
    # for interface
    stackid = input('Which stack do you want to delete? ')

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

@router.put("/history/{stackid}", tags=["history"])
def swt_stack(history: History, stackid=0):    
    # for interface
    stackid = input('Which stack do you want to switch to? ')

    try:
        history.stackdict[stackid]
        history.curstack = stackid
    except:
        return -1
