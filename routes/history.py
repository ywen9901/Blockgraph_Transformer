from internal.initialization import get_new_stackid
from model.static import scripts, designdict, stackdict, curstack, stackloc

from fastapi import APIRouter

router = APIRouter()

@router.post("/history/", tags=["history"])
def add_stack(id=0):
    newid = get_new_stackid('stack')
    stackdict[newid] = []
    stackdict[newid].append(stackloc[curstack])
    stackloc[newid] = stackloc[curstack]
    curstack = newid

@router.delete("/history/", tags=["history"])
def del_stack(stackid=0):
    # for interface
    stackid = input('Which stack do you want to delete? ')

    # delete all designs in this stack (execpt stack[0])
    for design in stackdict[stackid][1:]:
        del designdict[design]

    # update stack pointer if needed
    if curstack == stackid:
        stacklist = list(stackdict.keys())
        if stacklist.index(curstack) - 1 < 0:
            curstack = stacklist[stacklist.index(curstack) + 1]
        else:
            curstack = stacklist[stacklist.index(curstack) - 1]
    
    del stackdict[stackid]
    del stackloc[stackid]

@router.put("/history/{stackid}", tags=["history"])
def swt_stack(stackid=0):    
    # for interface
    stackid = input('Which stack do you want to switch to? ')

    try:
        stackdict[stackid]
        curstack = stackid
    except:
        return -1
