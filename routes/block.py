from internal.initialization import get_new_uuid, get_new_label
from model.static import Design

from fastapi import APIRouter

router = APIRouter()

@router.post("/block", tags=["block"])
def add_block(design: Design, target=0):
    blockid = get_new_uuid()
    blocklabel = get_new_label('block')
    design.blockdict[blockid] = {}
    design.labeldict[blockid] = blocklabel
    return blocklabel

@router.delete("/block", tags=["block"])
def del_block(design: Design, blockid=0):
    # for interface
    blockid = input('Which block do you want to delete? ')

    # update linkdict
    for _, portinfo in design.blockdict[blockid].items():
        if portinfo[0] == 'null':
            continue
        del design.linkdict[portinfo[0]][portinfo[1]]
    
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