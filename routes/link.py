from internal.initialization import get_new_uuid, get_new_label

from fastapi import APIRouter

router = APIRouter()

@router.post("/link/", tags=["link"])
def add_link(blockdict, linkdict, containerdict, groupdict, labeldict, target=0):
    linkid = get_new_uuid()
    linklabel = get_new_label('link')
    linkdict[linkid] = {}
    labeldict[linkid] = linklabel
    return linkid

@router.delete("/link/", tags=["link"])
def del_link(blockdict, linkdict, containerdict, groupdict, labeldict, linkid=0):
    global script

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
            del labeldict[ctn]
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
        del labeldict[gp]

    del linkdict[linkid]
    del labeldict[linkid]