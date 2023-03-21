from ..setup import scripts

def get_link_childrenblocks(linkdict, linkid):
    '''
    get all the blocks on this link
    '''
    result = []

    for link, linkinfo in linkdict.items():
        if link == linkid:
            for _, slotinfo in linkinfo.items():
                result.append(slotinfo[0])
            scripts.append('get_link_childrenblocks')
            return result # a list including all blocks

    return -1 # cannot find the link

def check_block_connection(blockdict, linkdict, containerdict, groupdict, blocklist):
    '''
    check if the blocks are connected to each others by the same link
    '''
    for link in linkdict.keys():
        conblocks = get_link_childrenblocks(linkdict, link)
        check = all(item in conblocks for item in blocklist)
        if check is True:
            scripts.append('check_block_connection')
            return link
    
    return -1 # the blocks are not connected by same link

def check_group_is_container(containerdict, groupdict, groupid): # doesn't check block connections, only match block id
    '''
    check if the group is a container or not
    '''
    groupitems = list(groupdict[groupid].keys())

    for ctn, ctninfo in containerdict.items():
        ctnitems = list(ctninfo['blockdict'].keys())
        if 'null' in ctnitems:
            ctnitems.remove('null')
        if sorted(ctnitems) == sorted(groupitems):
            scripts.append('check_group_is_container')
            return ctn
    
    return -1