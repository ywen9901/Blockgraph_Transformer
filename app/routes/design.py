from app.model.static import History

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/design/{designid}", tags=["design"])
def add_design(history: History, designid):
    try:
        history.designdict[designid] = {}
        history.stackdict[history.curstack].append(designid)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add design to designdict and stackdict")
    
    return history

@router.delete("/design/{designid}", tags=["design"])
def del_design(history: History, stackid, designid):
    try:
        history.stackdict[stackid].remove(designid)
        history.designdict.pop(designid)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete design")
    
    return history
