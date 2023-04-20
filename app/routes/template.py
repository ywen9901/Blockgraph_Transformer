from app.internal.initialization import get_new_uuid
from app.model.static import Design

from copy import deepcopy
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.put("/template/{blockid}/{templateid}", tags=["template"])
def block_expansion(design: Design, blockid, templateid):
    design.containerdict[blockid] = {}
    mapdict = {} # key: id in templatedict, value: new id

    # create a mapping dictionary between template id and container id
    for k in design.templatedict[templateid].keys():
        for blk, blkinfo in design.templatedict[templateid][k].items():
            if blk != "null":
                if mapdict.get(blk) == None:
                    mapdict[blk] = get_new_uuid()
                for port, portinfo in blkinfo.items():
                    if portinfo[0] != "null":
                        if mapdict.get(port) == None:
                            mapdict[port] = get_new_uuid()
                        if mapdict.get(portinfo[0]) == None:
                            mapdict[portinfo[0]] = get_new_uuid()
                        if mapdict.get(portinfo[1]) == None:
                            mapdict[portinfo[1]] = get_new_uuid()

    # add a new container
    for k in design.templatedict[templateid].keys():
        design.containerdict[blockid][k] = {}
        for blk, blkinfo in design.templatedict[templateid][k].items():
            design.containerdict[blockid][k][mapdict[blk]] = {}
            for port, portinfo in blkinfo.items():
                design.containerdict[blockid][k][mapdict[blk]][mapdict[port]] = [mapdict[portinfo[0]], mapdict[portinfo[1]]]

    # update the labeldict
    for k, v in mapdict.items():
        if k != "null":
            design.labeldict[v] = deepcopy(design.labeldict[k])

    # connect with bridge port/slot
    allport = list(design.blcokdict[blockid].keys())

    return design
