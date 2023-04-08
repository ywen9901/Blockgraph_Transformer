from internal.initialization import get_new_uuid, get_new_label
from model.static import Design

from fastapi import APIRouter

router = APIRouter()

@router.post("/link/", tags=["link"])
def add_link(design: Design, target=0):
    linkid = get_new_uuid()
    linklabel = get_new_label('link')
    design.linkdict[linkid] = {}
    design.labeldict[linkid] = linklabel
    return linkid

@router.delete("/link/", tags=["link"])
def del_link(design: Design, linkid=0):
    global script

    # for interface
    linkid = input('Which link do you want to delete? ')

    # update blockdict
    for link, linkinfo in design.linkdict.items():
        if link == linkid:
            for _, slotinfo in linkinfo.items():
                del design.blockdict[slotinfo[0]][slotinfo[1]]

    # update containerdict
    for ctn, ctninfo in design.containerdict.items():
        if linkid in list(ctninfo['linkdict'].keys()):
            del design.containerdict[ctn]
            del design.labeldict[ctn]
    try:
        del design.containerdict[linkid]
    except:
        pass

    # update groupdict
    tmp = []
    for gp, gpinfo in design.groupdict.items():
        if linkid in list(gpinfo.keys()):
            tmp.append(gp)
    for gp in tmp:
        del design.groupdict[gp]
        del design.labeldict[gp]

    del design.linkdict[linkid]
    del design.labeldict[linkid]