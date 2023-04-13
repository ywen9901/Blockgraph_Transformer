from app.internal.initialization import get_new_uuid, get_new_label
from app.model.static import Design, Connection

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/connection/", tags=["connection"])
def add_connection(design: Design, targets: Connection):
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

    design.blockdict[targets.block][newportid] = (targets.link, newslotid)
    design.linkdict[targets.link][newslotid] = (targets.block, newportid)

    return design

@router.delete("/connection", tags=["connection"])
def del_connection(design: Design, blockid: str, linkid: str): # targets = [blockname, linkname]
    # Check id exist
    if blockid not in design.blockdict:
        raise HTTPException(status_code=404, detail="Block ID not found")
    if linkid not in design.linkdict:
        raise HTTPException(status_code=404, detail="Link ID not found")
    
    # Check connection exist
    connection_exist = False

    for port, portinfo in design.blockdict[blockid].items():
        if portinfo[0] == linkid and design.linkdict[linkid][portinfo[1]][0] == blockid:
            connection_exist = True
            del design.blockdict[blockid][port]
            del design.linkdict[linkid][portinfo[1]]
            del design.labeldict[port]
            del design.labeldict[portinfo[1]]
            break

    if connection_exist is False:
        raise HTTPException(status_code=404, detail="No connection between the targets")

    return design