from .initialization import get_new_uuid, get_new_label
from .inspection import check_block_connection
from app.model.static import Design

from copy import deepcopy

def block_collapse(design: Design, groupid, parentblock): ######### need to be tested   
    ### done by group_collapse()
    # if groupid not in list(groupdict.keys()):
    #     return -1

    # parentblock = check_group_is_container(blockdict, linkdict, containerdict, groupdict, groupid)
    # if parentblock == -1:
    #     return -1
    ### done by group_collapse()   
    
    # TODO: many ports (need to consider all the blocks and the links that need to be collapsed)

    # update blockdict and linkdict
    newlinkid = get_new_uuid()
    newlinklabel = get_new_label('link')
    design.labeldict[newlinkid] = newlinklabel
    newslotid = get_new_uuid()
    newslotlabel = get_new_label('slot')
    design.labeldict[newslotid] = newslotlabel
    originalport = list(design.containerdict[parentblock]['blockdict']['null'].keys())[0] # bridge port
    design.blockdict[parentblock] = {originalport: (newlinkid, newslotid)}
    design.linkdict[newlinkid] = {newslotid: (parentblock, originalport)}

    childrenblocklist = list(design.groupdict[groupid].keys())
    for child in childrenblocklist:
        try:
            del design.blockdict[child]
        except:
            pass
    
    # update link item and slot item of other blocks in blockdict and in linkdict
    link = check_block_connection(design.blockdict, design.linkdict, design.containerdict, design.groupdict, childrenblocklist)
    if link == -1:
        print('The items are not in the same link.')
        return -1

    for block, blockinfo in design.blockdict.items():
        if list(blockinfo.values())[0][0] == link:
            newsid = get_new_uuid()
            newslabel = get_new_label('slot')
            design.labeldict[newsid] = newslabel
            design.blockdict[block][list(blockinfo.keys())[0]] = (newlinkid, newsid)
            design.linkdict[newlinkid][newsid] = (block, list(blockinfo.keys())[0])

    del design.linkdict[link]

    # delete group items which are collapsed
    delgroup = []
    for group, groupinfo in design.groupdict.items():
        for item in list(groupinfo.keys()):
            if item in childrenblocklist:
                delgroup.append(group)
                break
    for g in delgroup:
        del design.groupdict[g]
        del design.labeldict[g]

    return design

def link_collapse(design: Design, groupid, parentlink): ######### need to be tested
    # check containerdict
    ### done by group_collapse()
    # if groupid not in list(groupdict.keys()):
    #     return -1
    
    # parentlink = check_group_is_container(blockdict, linkdict, containerdict, groupdict, groupid)
    # if parentlink == -1:
    #     return -1
    ### done by group_collapse()
    
    childrenblocklist = list(design.containerdict[parentlink]['blockdict'].keys())
    
    # update blockdict and linkdict
    newlinkid = get_new_uuid()
    newlinklabel = get_new_label('link')
    design.labeldict[newlinkid] = newlinklabel
    design.linkdict[newlinkid] = {}
    for block in childrenblocklist:
        for _, portinfo in design.blockdict[block].items():
            for slot, slotinfo in design.linkdict[portinfo[0]].items():
                if slotinfo[0] != block:
                    design.blockdict[slotinfo[0]][slotinfo[1]] = (newlinkid, slot)
                    design.linkdict[newlinkid][slot] = deepcopy(slotinfo)
    for block in childrenblocklist:
        for _, portinfo in design.blockdict[block].items():
            del design.linkdict[portinfo[0]]
        del design.blockdict[block]
    
    # update containerdict
    design.containerdict[newlinkid] = deepcopy(design.containerdict[parentlink])
    del design.containerdict[parentlink]

    # delete group items which are collapsed
    delgroup = []
    for group, groupinfo in design.groupdict.items():
        for item in list(groupinfo.keys()):
            if item in childrenblocklist:
                delgroup.append(group)
                break
    for g in delgroup:
        del design.groupdict[g]
        del design.labeldict[g]

    return design