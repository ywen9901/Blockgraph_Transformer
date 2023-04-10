from app.internal.initialization import get_new_uuid, get_new_label
from app.model.static import Design, Container

from copy import deepcopy
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/block_container", tags=["container"])
def add_block_container(design: Design, targets: Container):
    if targets.parent not in design.blockdict:
        raise HTTPException(status_code=404, detail="Block ID {} not found in blockdict".format(targets.parent))
    for target in targets.inner:
        if target not in design.blockdict:
            raise HTTPException(status_code=404, detail="Block ID {} not found in blockdict".format(target))
    
    parentblock = targets.parent
    childrenblocklist = targets.inner
    # childrenblocklist = childrenblock.split(', ')
    childrenblocklist.append('null')

    tmpblockdict = {}
    tmplinkdict = {}
    
    try:
        newlinkid = get_new_uuid()
        newlinklabel = get_new_label('link')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create new link ID and label")

    design.labeldict[newlinkid] = newlinklabel
    tmplinkdict[newlinkid] = {}

    for block in childrenblocklist:
        tmpblockdict[block] = {}
        
        try:
            newslotid = get_new_uuid()
            newslotlabel = get_new_label('slot')
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to create new slot ID and label")

        design.labeldict[newslotid] = newslotlabel
        
        
        try:
            newportid = get_new_uuid()
            newportlabel = get_new_label('port')
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to create new port ID and label")
    
        design.labeldict[newportid] = newportlabel
        tmpblockdict[block][newportid] = (newlinkid, newslotid)
        tmplinkdict[newlinkid][newslotid] = (block, newportid)
    
    design.containerdict[parentblock] = {'blockdict': tmpblockdict, 'linkdict': tmplinkdict}
    return design



@router.post("/link_container", tags=["container"])
def add_link_container(design: Design, targets: Container):
    if targets.parent not in design.linkdict:
        raise HTTPException(status_code=404, detail="Link ID {} not found in linkdict".format(targets.parent))
    for target in targets.inner:
        if target not in design.linkdict:
            raise HTTPException(status_code=404, detail="Link ID {} not found in linkdict".format(target))
    
    parentlink = targets.parent
    innerblocks = targets.inner
    # childrenblocklist = innerblocks.split(', ')
    if parentlink in list(design.linkdict.keys()):
        outterslot = list(design.linkdict[parentlink].keys())
    else:
        try:
            newslotid1 = get_new_uuid()
            newslotlabel1 = get_new_label('slot')
            newslotid2 = get_new_uuid()
            newslotlabel2 = get_new_label('slot')
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to create new slot ID and label")
    
        design.labeldict[newslotid1] = newslotlabel1
        design.labeldict[newslotid2] = newslotlabel2
        outterslot = [newslotid1, newslotid2]

    tmpblockdict = {}
    tmplinkdict = {}
    
    try:
        newlinkid1 = get_new_uuid()
        newlinklabel1 = get_new_label('link')
        newlinkid2 = get_new_uuid()
        newlinklabel2 = get_new_label('link')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create new link ID and label")

    design.labeldict[newlinkid1] = newlinklabel1
    design.labeldict[newlinkid2] = newlinklabel2
    tmplinkdict[newlinkid1] = {}

    for block in innerblocks:
        tmplinkdict[newlinkid2] = {}
        tmpblockdict[block] = {}

        if innerblocks.index(block) == 0: # first block
            tmplinkdict[newlinkid1][outterslot[0]] = ('null', 'null')

        try:
            newpid1 = get_new_uuid()
            newpid2 = get_new_uuid()
            newsid1 = get_new_uuid()
            newsid2 = get_new_uuid()
            newplabel1 = get_new_label('port')
            newplabel2 = get_new_label('port')
            newslabel1 = get_new_label('slot')
            newslabel2 = get_new_label('slot')
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to create new ID and label for innerblocks")

        design.labeldict[newpid1] = newplabel1
        design.labeldict[newpid2] = newplabel2
        design.labeldict[newsid1] = newslabel1
        design.labeldict[newsid2] = newslabel2
        tmpblockdict[block][newpid1] = (newlinkid1, newsid1)
        tmpblockdict[block][newpid2] = (newlinkid2, newsid2)
        tmplinkdict[newlinkid1][newsid1] = (block, newpid1)
        tmplinkdict[newlinkid2][newsid2] = (block, newpid2)

        if innerblocks.index(block) == len(innerblocks) - 1: # last block
            tmplinkdict[newlinkid2][outterslot[1]] = ('null', 'null')
        
        newlinkid1 = newlinkid2
        try:
            newlinkid2 = get_new_uuid()
            newlinklabel2 = get_new_label('link')
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to create new link ID and label")
        
        design.labeldict[newlinkid2] = newlinklabel2

    design.containerdict[parentlink] = (tmpblockdict, tmplinkdict)
    return design

@router.delete("/container/{containerid}", tags=["container"])
def del_container(design: Design, containerid):
    try:
        del design.containerdict[containerid]
        del design.labeldict[containerid]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete container in containerdict and labeldict")
    
    return design