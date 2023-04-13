from app.internal.initialization import get_new_uuid, get_new_label
from app.model.static import Design

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/link/", tags=["link"])
def add_link(design: Design):
    try:
        linkid = get_new_uuid()
        linklabel = get_new_label('link')
    except:
        raise HTTPException(status_code=500, detail="Failed to create new link ID and label")
    
    design.linkdict[linkid] = {}
    design.labeldict[linkid] = linklabel
    return design

@router.delete("/link/{linkid}", tags=["link"])
def del_link(design: Design, linkid):
    if linkid not in design.linkdict:
        raise HTTPException(status_code=404, detail="Link ID not found")
    
    # update blockdict
    # for link, linkinfo in design.linkdict.items():
    #     if link == linkid:
    #         for _, slotinfo in linkinfo.items():
    #             del design.blockdict[slotinfo[0]][slotinfo[1]]
    for slot, slotinfo in design.linkdict[linkid].items():
        if slotinfo[0] == 'null':
            continue
        del design.blockdict[slotinfo[0]][slotinfo[1]]
        del design.labeldict[slot]
        del design.labeldict[slotinfo[0]]
        del design.labeldict[slotinfo[1]]

    # update containerdict
    for ctn, ctninfo in design.containerdict.items():
        if linkid in list(ctninfo['linkdict'].keys()):
            del design.containerdict[ctn]
            del design.labeldict[ctn]
    try:
        del design.containerdict[linkid]
    except:
        pass

    # update groupdict
    tmp = []
    for gp, gpinfo in design.groupdict.items():
        if linkid in list(gpinfo.keys()):
            tmp.append(gp)
    for gp in tmp:
        del design.groupdict[gp]
        del design.labeldict[gp]

    del design.linkdict[linkid]
    del design.labeldict[linkid]
    
    return design

