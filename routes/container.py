from internal.initialization import get_new_uuid, get_new_label
from model.static import Design

from copy import deepcopy
from fastapi import APIRouter

router = APIRouter()

@router.post("/block_container", tags=["container"])
def add_block_container(design: Design, targets=0):
    parentblock = targets[0]
    childrenblocklist = targets[1:]
    # childrenblocklist = childrenblock.split(', ')
    childrenblocklist.append('null')

    tmpblockdict = {}
    tmplinkdict = {}
    newlinkid = get_new_uuid()
    newlinklabel = get_new_label('link')
    design.labeldict[newlinkid] = newlinklabel
    tmplinkdict[newlinkid] = {}

    for block in childrenblocklist:
        tmpblockdict[block] = {}
        newslotid = get_new_uuid()
        newslotlabel = get_new_label('slot')
        design.labeldict[newslotid] = newslotlabel
        newportid = get_new_uuid()
        newportlabel = get_new_label('port')
        design.labeldict[newportid] = newportlabel
        tmpblockdict[block][newportid] = (newlinkid, newslotid)
        tmplinkdict[newlinkid][newslotid] = (block, newportid)
    
    design.containerdict[parentblock] = {'blockdict': tmpblockdict, 'linkdict': tmplinkdict}

##############
# Conflict
##############

@router.post("/link_container", tags=["container"])
def add_link_container(design: Design, targets=0):
    parentlink = targets[0]
    innerblocks = targets[1:]
    # childrenblocklist = innerblocks.split(', ')
    if parentlink in list(design.linkdict.keys()):
        outterslot = list(design.linkdict[parentlink].keys())
    else:
        newslotid1 = get_new_uuid()
        newslotlabel1 = get_new_label('slot')
        design.labeldict[newslotid1] = newslotlabel1
        newslotid2 = get_new_uuid()
        newslotlabel2 = get_new_label('slot')
        design.labeldict[newslotid2] = newslotlabel2
        outterslot = [newslotid1, newslotid2]

    tmpblockdict = {}
    tmplinkdict = {}
    newlinkid1 = get_new_uuid()
    newlinklabel1 = get_new_label('link')
    design.labeldict[newlinkid1] = newlinklabel1
    newlinkid2 = get_new_uuid()
    newlinklabel2 = get_new_label('link')
    design.labeldict[newlinkid2] = newlinklabel2
    tmplinkdict[newlinkid1] = {}

    for block in innerblocks:
        tmplinkdict[newlinkid2] = {}
        tmpblockdict[block] = {}

        if innerblocks.index(block) == 0: # first block
            tmplinkdict[newlinkid1][outterslot[0]] = ('null', 'null')

        newpid1 = get_new_uuid()
        newpid2 = get_new_uuid()
        newsid1 = get_new_uuid()
        newsid2 = get_new_uuid()
        newplabel1 = get_new_label('port')
        newplabel2 = get_new_label('port')
        newslabel1 = get_new_label('slot')
        newslabel2 = get_new_label('slot')
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
        newlinkid2 = get_new_uuid()
        newlinklabel2 = get_new_label('link')
        design.labeldict[newlinkid2] = newlinklabel2

    design.containerdict[parentlink] = (tmpblockdict, tmplinkdict)

@router.delete("/container/{containerid}", tags=["container"])
def del_container(design: Design, containerid=0):
    try:
        del design.containerdict[containerid]
        del design.labeldict[containerid]
    except:
        return -1