from model.static import scripts

from copy import deepcopy
from fastapi import APIRouter

router = APIRouter()

@router.post("/container/", tags=["container"])
def add_block_container(blockdict, linkdict, containerdict, groupdict, targets=0):

    # for interface
    tmp = input('Please input the information: (format: parent block, child block 1, child block 2, ...) ')
    targets = tmp.split(', ')

    parentblock = targets[0]
    childrenblocklist = targets[1:]
    # childrenblocklist = childrenblock.split(', ')
    childrenblocklist.append('null')

    tmpblockdict = {}
    tmplinkdict = {}
    newlinkid = get_new_id('link')
    tmplinkdict[newlinkid] = {}

    for block in childrenblocklist:
        tmpblockdict[block] = {}
        newslotid = get_new_id('slot')
        newportid = get_new_id('port')
        tmpblockdict[block][newportid] = (newlinkid, newslotid)
        tmplinkdict[newlinkid][newslotid] = (block, newportid)
    
    containerdict[parentblock] = {'blockdict': tmpblockdict, 'linkdict': tmplinkdict}
    scripts.append('add_block_container')

##############
# Conflict
##############

# @router.post("/container/", tags=["container"])
# def add_link_container(blockdict, linkdict, containerdict, groupdict, targets=0):

#     # for interface
#     tmp = input('Please input the information: (format: parent link, child block 1, child block 2, ...) ')
#     targets = tmp.split(', ')

#     parentlink = targets[0]
#     innerblocks = targets[1:]
#     # childrenblocklist = innerblocks.split(', ')
#     if parentlink in list(linkdict.keys()):
#         outterslot = list(linkdict[parentlink].keys())
#     else:
#         newslotid1 = get_new_id('slot')
#         newslotid2 = get_new_id('slot')
#         outterslot = [newslotid1, newslotid2]

#     tmpblockdict = {}
#     tmplinkdict = {}
#     newlinkid1 = get_new_id('link')
#     newlinkid2 = get_new_id('link')
#     tmplinkdict[newlinkid1] = {}

#     for block in innerblocks:
#         tmplinkdict[newlinkid2] = {}
#         tmpblockdict[block] = {}

#         if innerblocks.index(block) == 0: # first block
#             tmplinkdict[newlinkid1][outterslot[0]] = ('null', 'null')

#         newpid1 = get_new_id('port')
#         newpid2 = get_new_id('port')
#         newsid1 = get_new_id('slot')
#         newsid2 = get_new_id('slot')
#         tmpblockdict[block][newpid1] = (newlinkid1, newsid1)
#         tmpblockdict[block][newpid2] = (newlinkid2, newsid2)
#         tmplinkdict[newlinkid1][newsid1] = (block, newpid1)
#         tmplinkdict[newlinkid2][newsid2] = (block, newpid2)

#         if innerblocks.index(block) == len(innerblocks) - 1: # last block
#             tmplinkdict[newlinkid2][outterslot[1]] = ('null', 'null')
        
#         newlinkid1 = newlinkid2
#         newlinkid2 = get_new_id('link')

#     containerdict[parentlink] = (tmpblockdict, tmplinkdict)
#     scripts.append('add_link_container')

@router.delete("/container/", tags=["container"])
def del_container(blockdict, linkdict, containerdict, groupdict, containerid=0):

    # for interface
    containerid = input('Which container do you want to delete? ')

    try:
        del containerdict[containerid]
    except:
        return -1
    
    scripts.append('del_container')

@router.put("/container/{blockid}", tags=["container"])
def block_expansion(blockdict, linkdict, containerdict, groupdict, blockid=0):
    links = []

    # for interface
    blockid = input('Which block do you want to expand? ')

    # find the links connect to the block
    for _, portinfo in blockdict[blockid].items():
        links.append(portinfo[0])
    
    # update blockdict
    for block, blockinfo in containerdict[blockid]['blockdict'].items():
        if block != 'null':
            tmp = deepcopy(blockinfo) # won't update the values in containerdict
            blockdict[block] = tmp
    del blockdict[blockid]

    # update linkdict
    ## container link
    newlinkitem = deepcopy(containerdict[blockid]['linkdict'])
    for link, linkinfo in newlinkitem.items():
        for slot, slotinfo in linkinfo.items():
            if slotinfo[0] == 'null':
                del newlinkitem[link][slot]
                linkdict[link] = newlinkitem[link]
                break
    
    ## original link
    linkinfo = containerdict[blockid]['linkdict'].values()
    linkinfo = list(linkinfo)[0]
    newblocktuple = []
    for _, slotinfo in linkinfo.items():
        if slotinfo[0] != 'null':from copy import deepcopy

@router.put("/container/{linkid}", tags=["container"])
def link_expansion(blockdict, linkdict, containerdict, groupdict, linkid=0):

    # for interface
    linkid = input('Which link do you want to expand? ')

    for block, blockinfo in containerdict[linkid]['blockdict'].items():
        blockdict[block] = deepcopy(blockinfo)

    for _, linkinfo in containerdict[linkid]['linkdict'].items():
        newlinkid = get_new_id('link')
        linkdict[newlinkid] = {}
        for slot, slotinfo in linkinfo.items():
            if slotinfo == ('null', 'null'):
                linkdict[newlinkid][slot] = deepcopy(linkdict[linkid][slot])
            else:
                linkdict[newlinkid][slot] = deepcopy(slotinfo)
            block = linkdict[newlinkid][slot][0]
            port = linkdict[newlinkid][slot][1]
            blockdict[block][port] = (newlinkid, slot)
    
    del linkdict[linkid]
    globalvar.scripts.append('link_expansion')
