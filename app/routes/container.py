from app.internal.initialization import get_new_uuid, get_new_label
from app.model.static import Design

from copy import deepcopy
from pydantic import conlist
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/block_container", tags=["container"])
def add_block_container(design: Design, targets: conlist(str, min_items=1)):
    if targets[0] not in design.blockdict:
        raise HTTPException(status_code=404, detail="Block ID {} not found in blockdict".format(targets.parent))
    for target in targets[1:]:
        if target not in design.blockdict:
            raise HTTPException(status_code=404, detail="Block ID {} not found in blockdict".format(target))
    
    parentblock = targets[0]
    childrenblocklist = targets[1:]
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
def add_link_container(design: Design, targets: conlist(str, min_items=1)):
    if targets[0] not in design.linkdict:
        raise HTTPException(status_code=404, detail="Link ID {} not found in linkdict".format(targets[0]))
    for target in targets[1:]:
        if target not in design.linkdict:
            raise HTTPException(status_code=404, detail="Link ID {} not found in linkdict".format(target))
    
    parentlink = targets[0]
    innerblocks = targets[1:]
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
    if containerid not in design.containerdict:
        raise HTTPException(status_code=404, detail="Container ID not found")
    
    try:
        del design.labeldict
        del design.containerdict[containerid]
        del design.labeldict[containerid]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete the container")
    
    return design

@router.put("/block_container", tags=["container"])
def block_flattening(design: Design, blockid):
    links = []

    # find the links connect to the block
    for _, portinfo in design.blockdict[blockid].items():
        links.append(portinfo[0])
    
    # update blockdict
    for block, blockinfo in design.containerdict[blockid]['blockdict'].items():
        if block != 'null':
            tmp = deepcopy(blockinfo) # won't update the values in containerdict
            design.blockdict[block] = tmp
    del design.blockdict[blockid]

    # update linkdict
    ## keep container link
    # newlinkitem = deepcopy(containerdict[blockid]['linkdict'])
    # for link, linkinfo in newlinkitem.items():
    #     for slot, slotinfo in linkinfo.items():
    #         if slotinfo[0] == 'null':
    #             del newlinkitem[link][slot]
    #             linkdict[link] = newlinkitem[link]
    #             break
    
    ## original link
    linkinfo = design.containerdict[blockid]['linkdict'].values()
    linkinfo = list(linkinfo)[0]
    newblocktuple = []
    for _, slotinfo in linkinfo.items():
        if slotinfo[0] != 'null':
            newblocktuple.append(slotinfo)

    for link in links:
        totalblocktuple = newblocktuple
        for _, blockinfo in design.linkdict[link].items():
            if blockinfo[0] != blockid:
                totalblocktuple.append(blockinfo)
        del design.linkdict[link]
        newlinkid = get_new_uuid()
        newlinklabel = get_new_label('link')
        design.linkdict[newlinkid] = {}
        design.labeldict[newlinkid] = newlinklabel
        for i in range(len(totalblocktuple)):
            newslotid = get_new_uuid()
            newslotlabel = get_new_label('slot')
            design.linkdict[newlinkid][newslotid] = totalblocktuple[i]
            design.labeldict[newslotid] = newslotlabel

            # update other blocks in blockdict
            design.blockdict[totalblocktuple[i][0]][totalblocktuple[i][1]] = (newlinkid, newslotid)
    
    del design.containerdict[blockid]

    return design

@router.put("/link_container", tags=["container"])
def link_flattening(design: Design, linkid=0):
    # for interface
    linkid = input('Which link do you want to flatten? ')

    for block, blockinfo in design.containerdict[linkid]['blockdict'].items():
        design.blockdict[block] = deepcopy(blockinfo)

    for _, linkinfo in design.containerdict[linkid]['linkdict'].items():
        newlinkid = get_new_uuid()
        newlinklabel = get_new_label('link')
        design.labeldict[newlinkid] = newlinklabel
        design.linkdict[newlinkid] = {}
        for slot, slotinfo in linkinfo.items():
            if slotinfo == ('null', 'null'):
                design.linkdict[newlinkid][slot] = deepcopy(design.linkdict[linkid][slot])
            else:
                design.linkdict[newlinkid][slot] = deepcopy(slotinfo)
            block = design.linkdict[newlinkid][slot][0]
            port = design.linkdict[newlinkid][slot][1]
            design.blockdict[block][port] = (newlinkid, slot)
    
    del design.linkdict[linkid]
    del design.containerdict[linkid]

    return design