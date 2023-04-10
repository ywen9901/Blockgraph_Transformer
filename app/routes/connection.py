from internal.initialization import get_new_uuid, get_new_label
from model.static import Design

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/connection/", tags=["connection"])
def add_connection(design: Design, targets: list):
    try:
        newportid = get_new_uuid()
        newportlabel = get_new_label('port')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create new port ID and label")
    
    design.labeldict[newportid] = newportlabel

    try:
        newslotid = get_new_uuid()
        newslotlabel = get_new_label('slot')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create new slot ID and label")
    
    design.labeldict[newslotid] = newslotlabel

    design.blockdict[targets[0]][newportid] = (targets[1], newslotid)
    design.linkdict[targets[1]][newslotid] = (targets[0], newportid)

    return design

@router.delete("/connection", tags=["connection"])
def del_connection(design: Design, targets: list): # targets = [blockname, linkname]
    if targets[0] not in design.blockdict:
        raise HTTPException(status_code=404, detail="Block ID not found in blockdict")
    if targets[1] not in design.linkdict:
        raise HTTPException(status_code=404, detail="Link ID not found in linkdict")
    
    slotid = ''
    portid = ''

    for port, portinfo in design.blockdict[targets[0]].items():
        if portinfo[0] == targets[1]:
            slotid = portinfo[1]
            portid = port
            break
    
    del design.blockdict[targets[0]][portid]
    del design.linkdict[targets[1]][slotid]
    del design.labeldict[portid]
    del design.labeldict[slotid]

    return design