from internal.initialization import get_new_uuid, get_new_label
from internal.inspection import check_group_is_container
from internal.collapsion import block_collapse, link_collapse

from model.static import Design

from fastapi import APIRouter

router = APIRouter()

@router.post("/group/", tags=["group"])
def add_group(design: Design, itemlist=0):
    # for interface
    tmp = input('Which items do you want to group? (format: item 1, item 2, ...) ')
    itemlist = tmp.split(', ')

    newgroupid = get_new_uuid()
    newgrouplabel = get_new_label('group')
    design.labeldict[newgroupid] = newgrouplabel

    tmp = {}
    for item in itemlist:
        try:
            tmp[item] = design.blockdict[item]
        except:
            try:
                tmp[item] = design.linkdict[item]
            except:
                return -1
    
    design.groupdict[newgroupid] = tmp

@router.put("/group/{groupid}", tags=["group"])
def group_collapse(design: Design, groupid=0): # for interface
    groupid = input('Which group do you want to collapse? ')
    if groupid not in list(design.groupdict.keys()):
        print('Can\'t find group.')
        return -1
    
    parent = check_group_is_container(design.containerdict, design.groupdict, groupid)
    if parent == -1:
        print('Can\'t find container.')
        return -1

    if '_b' in parent:
        print('Do block collapse')
        block_collapse(design.blockdict, design.linkdict, design.containerdict, design.groupdict, design.labeldict, groupid, parent)
    elif '_l' in parent:
        print('Do link collapse')
        link_collapse(design.blockdict, design.linkdict, design.containerdict, design.groupdict, design.labeldict, groupid, parent)
    else:
        return -1

@router.delete("/group/{groupid}", tags=["group"])
def del_group(design: Design, groupid=0):
    try:
        del design.groupdict[groupid]
        del design.labeldict[groupid]
    except:
        return -1

