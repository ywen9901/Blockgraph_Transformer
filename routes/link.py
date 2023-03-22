from internal.initialization import get_new_id
from model.static import scripts

from fastapi import APIRouter

router = APIRouter()

@router.post("/link/", tags=["link"])
def add_link(blockdict, linkdict, containerdict, groupdict, target=0):
    linkid = get_new_id('link')
    linkdict[linkid] = {}

    scripts.append('add_link')
    return linkid

@router.delete("/link/", tags=["link"])
def del_link(blockdict, linkdict, containerdict, groupdict, linkid=0):
    # for interface
    linkid = input('Which link do you want to delete? ')

    # update blockdict
    for link, linkinfo in linkdict.items():
        if link == linkid:
            for _, slotinfo in linkinfo.items():
                del blockdict[slotinfo[0]][slotinfo[1]]

    # update containerdict
    for ctn, ctninfo in containerdict.items():
        if linkid in list(ctninfo['linkdict'].keys()):
            del containerdict[ctn]
    try:
        del containerdict[linkid]
    except:
        pass

    # update groupdict
    tmp = []
    for gp, gpinfo in groupdict.items():
        if linkid in list(gpinfo.keys()):
            tmp.append(gp)
    for gp in tmp:
        del groupdict[gp]

    del linkdict[linkid]

    scripts.append('del_link')
