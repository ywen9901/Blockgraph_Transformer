from internal.initialization import get_new_id
from .static import scripts

from fastapi import APIRouter

router = APIRouter()

@router.get("/block/", tags=["block"])
def get_blocks():
    pass

@router.get("/block/{blockid}", tags=["block"])
def get_block(blockid: str):
    pass

@router.post("/block/", tags=["block"])
def add_block(blockdict, linkdict, containerdict, groupdict, target=0):
    blockid = get_new_id('block')
    blockdict[blockid] = {}

    scripts.append('add_block')
    return blockid

@router.delete("/block/", tags=["block"])
def del_block(blockdict, linkdict, containerdict, groupdict, blockid=0):
    # for interface
    blockid = input('Which block do you want to delete? ')

    # update linkdict
    for _, portinfo in blockdict[blockid].items():
        del linkdict[portinfo[0]][portinfo[1]]
    
    # update containerdict
    for ctn, ctninfo in containerdict.items():
        if blockid in list(ctninfo['blockdict'].keys()):
            del containerdict[ctn]
    try:
        del containerdict[blockid]
    except:
        pass

    # update groupdict
    tmp = []
    for gp, gpinfo in groupdict.items():
        if blockid in list(gpinfo.keys()):
            tmp.append(gp)
    for gp in tmp:
        del groupdict[gp]

    del blockdict[blockid]

    scripts.append('del_block')
