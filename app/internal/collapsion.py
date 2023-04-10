from .initialization import get_new_uuid, get_new_label
from .inspection import check_block_connection

from copy import deepcopy

def block_collapse(blockdict, linkdict, containerdict, groupdict, labeldict, groupid=0, parentblock=0): ######### need to be tested    
    # TODO: many ports (need to consider all the blocks and the links that need to be collapsed)

    # update blockdict and linkdict
    newlinkid = get_new_uuid()
    newlinklabel = get_new_label('link')
    labeldict[newlinkid] = newlinklabel
    newslotid = get_new_uuid()
    newslotlabel = get_new_label('slot')
    labeldict[newslotid] = newslotlabel
    originalport = list(containerdict[parentblock]['blockdict']['null'].keys())[0] # bridge port
    blockdict[parentblock] = {originalport: (newlinkid, newslotid)}
    linkdict[newlinkid] = {newslotid: (parentblock, originalport)}

    childrenblocklist = list(groupdict[groupid].keys())
    for child in childrenblocklist:
        try:
            del blockdict[child]
        except:
            pass
    
    # update link item and slot item of other blocks in blockdict and in linkdict
    link = check_block_connection(blockdict, linkdict, containerdict, groupdict, childrenblocklist)
    if link == -1:
        print('The items are not in the same link.')
        return -1

    for block, blockinfo in blockdict.items():
        if list(blockinfo.values())[0][0] == link:
            newsid = get_new_uuid()
            newslabel = get_new_label('slot')
            labeldict[newsid] = newslabel
            blockdict[block][list(blockinfo.keys())[0]] = (newlinkid, newsid)
            linkdict[newlinkid][newsid] = (block, list(blockinfo.keys())[0])

    del linkdict[link]

    # delete group items which are collapsed
    delgroup = []
    for group, groupinfo in groupdict.items():
        for item in list(groupinfo.keys()):
            if item in childrenblocklist:
                delgroup.append(group)
                break
    for g in delgroup:
        del groupdict[g]
        del labeldict[g]

def link_collapse(blockdict, linkdict, containerdict, groupdict, labeldict, groupid=0, parentlink=0): ######### need to be tested  
    childrenblocklist = list(containerdict[parentlink]['blockdict'].keys())
    
    # update blockdict and linkdict
    newlinkid = get_new_uuid()
    newlinklabel = get_new_label('link')
    labeldict[newlinkid] = newlinklabel
    linkdict[newlinkid] = {}
    for block in childrenblocklist:
        for _, portinfo in blockdict[block].items():
            for slot, slotinfo in linkdict[portinfo[0]].items():
                if slotinfo[0] != block:
                    blockdict[slotinfo[0]][slotinfo[1]] = (newlinkid, slot)
                    linkdict[newlinkid][slot] = deepcopy(slotinfo)
    for block in childrenblocklist:
        for _, portinfo in blockdict[block].items():
            del linkdict[portinfo[0]]
        del blockdict[block]
    
    # update containerdict
    containerdict[newlinkid] = deepcopy(containerdict[parentlink])
    del containerdict[parentlink]

    # delete group items which are collapsed
    delgroup = []
    for group, groupinfo in groupdict.items():
        for item in list(groupinfo.keys()):
            if item in childrenblocklist:
                delgroup.append(group)
                break
    for g in delgroup:
        del groupdict[g]
        del labeldict[g]