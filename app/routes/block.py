from app.internal.initialization import get_new_uuid, get_new_label
from app.model.static import Design

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

router = APIRouter()

@router.post("/block", tags=["block"])
def add_block(design: Design):
    try:
        blockid = get_new_uuid()
        blocklabel = get_new_label('block')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create new block ID and label")
    
    if design.blockdict and design.labeldict:
        if blockid in design.blockdict or blockid in design.labeldict:
            raise HTTPException(status_code=500, detail="Duplicated ID")
    
    design.blockdict[blockid] = {}
    design.labeldict[blockid] = blocklabel
    
    return design

@router.delete("/block/{blockid}", tags=["block"])
def del_block(design: Design, blockid: str):
    if blockid not in design.blockdict:
        raise HTTPException(status_code=404, detail="Block ID not found in blockdict")
    
    # update linkdict and labeldict
    for port, portinfo in design.blockdict[blockid].items():
        if portinfo[0] == 'null':
            continue
        del design.linkdict[portinfo[0]][portinfo[1]]
        del design.labeldict[port]
        del design.labeldict[portinfo[0]]
        del design.labeldict[portinfo[1]]
    
    # update containerdict
    for ctn, ctninfo in design.containerdict.items():
        if blockid in list(ctninfo['blockdict'].keys()):
            del design.containerdict[ctn]
    try:
        del design.containerdict[blockid]
    except:
        pass

    # update groupdict
    tmp = []
    for gp, gpinfo in design.groupdict.items():
        if blockid in list(gpinfo.keys()):
            tmp.append(gp)
    for gp in tmp:
        del design.groupdict[gp]
        del design.labeldict[gp]

    del design.blockdict[blockid]
    del design.labeldict[blockid]

    #update labeldict

    return design