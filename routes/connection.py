from internal.initialization import get_new_uuid, get_new_label

from fastapi import APIRouter

router = APIRouter()

@router.post("/connection/", tags=["connection"])
def add_connection(blockdict, linkdict, containerdict, groupdict, labeldict, targets=0): # targets = [blockname, linkname]
    # for interface
    tmp = input('Which connection do you want to add? (format: blockname, linkname) ')
    targets = tmp.split(', ')
    
    newportid = get_new_uuid()
    newportlabel = get_new_label('port')
    labeldict[newportid] = newportlabel

    newslotid = get_new_uuid()
    newslotlabel = get_new_label('slot')
    labeldict[newslotid] = newslotlabel

    blockdict[targets[0]][newportid] = (targets[1], newslotid)
    linkdict[targets[1]][newslotid] = (targets[0], newportid)

@router.delete("/connection/{}", tags=["connection"])
def del_connection(blockdict, linkdict, containerdict, groupdict, labeldict, targets=0): # targets = [blockname, linkname]
    # for interface
    tmp = input('Which connection do you want to delete? (format: blockname, linkanme) ')
    targets = tmp.split(', ')
    
    slotid = ''
    portid = ''

    for port, portinfo in blockdict[targets[0]].items():
        if portinfo[0] == targets[1]:
            slotid = portinfo[1]
            portid = port
            break
    
    del blockdict[targets[0]][portid]
    del linkdict[targets[1]][slotid]
    del labeldict[portid]
    del labeldict[slotid]
