from internal.initialization import get_new_uuid, get_new_label
from model.static import Design

from fastapi import APIRouter

router = APIRouter()

# @router.put("/connection/", tags=["connection"])
# def get_connection(design: Design):
#     return design.blockdict

# Create a new connection
@router.post("/connection/", tags=["connection"])
def add_connection(design: Design, targets: list):
    
    newportid = get_new_uuid()
    newportlabel = get_new_label('port')
    design.labeldict[newportid] = newportlabel

    newslotid = get_new_uuid()
    newslotlabel = get_new_label('slot')
    design.labeldict[newslotid] = newslotlabel

    design.blockdict[targets[0]][newportid] = (targets[1], newslotid)
    design.linkdict[targets[1]][newslotid] = (targets[0], newportid)

@router.delete("/connection", tags=["connection"])
def del_connection(design: Design, targets: list): # targets = [blockname, linkname]
   
    slotid = ''
    portid = ''

    for port, portinfo in design.blockdict[targets[0]].items():
        if portinfo[0] == targets[1]:
            slotid = portinfo[1]
            portid = port
            break
    
    del design.blockdict[targets[0]][portid]
    del design.linkdict[targets[1]][slotid]
    del design.labeldict[portid]
    del design.labeldict[slotid]
