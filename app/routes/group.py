from pydantic import conlist
from app.internal.initialization import get_new_uuid, get_new_label
from app.internal.inspection import check_group_is_container
from app.internal.collapsion import block_collapse, link_collapse

from app.model.static import Design

from copy import deepcopy
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/group", tags=["group"])
def add_group(design: Design, itemlist: conlist(str, min_items=1)):
    try:
        newgroupid = get_new_uuid()
        newgrouplabel = get_new_label('group')
        design.labeldict[newgroupid] = newgrouplabel
    except:
        raise HTTPException(status_code=500, detail="Failed to create new group ID and label")

    tmp = {}
    for item in itemlist:
        try:
            tmp[item] = design.blockdict[item]
        except:
            try:
                tmp[item] = design.linkdict[item]
            except:
                raise HTTPException(status_code=404, detail="Item not found in blockdict or linkdict")
    
    design.groupdict[newgroupid] = tmp
    return design

@router.put("/group/{groupid}", tags=["group"])
def group_collapse(design: Design, groupid): # for interface
    if groupid not in list(design.groupdict.keys()):
        raise HTTPException(status_code=404, detail="Group ID not found")
    
    parent = check_group_is_container(design.containerdict, design.groupdict, groupid)
    if parent == -1:
        raise HTTPException(status_code=422, detail="Group is not container")

    if '_b' in parent:
        design = block_collapse(design, groupid, parent)
    elif '_l' in parent:
        design = link_collapse(design.blockdict, design.linkdict, design.containerdict, design.groupdict, design.labeldict, groupid, parent)
    else:
        raise HTTPException(status_code=422, detail="Container name error")

    return design
    
@router.delete("/group/{groupid}", tags=["group"])
def del_group(design: Design, groupid):
    try:
        del design.groupdict[groupid]
        del design.labeldict[groupid]
    except:
        raise HTTPException(status_code=500, detail="Failed to delete group")
    
    return design

