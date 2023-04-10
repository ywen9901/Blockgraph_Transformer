import uuid
from app.model.example import infodict
from app.model.static import tfidx, stackidx

def get_key(dic, val): 
    for k, v in dic.items():
        if v == val:
            return k
    
    return -1

def iterate_dict(infodict, dic):
    readabledict = {}
    infodict['labeldict']['null'] = "null"

    for item, iteminfo in dic.items():
        readabledict[infodict['labeldict'][item]] = {}
        for sub, subinfo in iteminfo.items():
            readabledict[infodict['labeldict'][item]][infodict['labeldict'][sub]] = [infodict['labeldict'][subinfo[0]], infodict['labeldict'][subinfo[1]]]

    return readabledict

def v_label(infodict):
    readabledict = {}

    # blockdict & linkdict
    readabledict['blockdict'] = iterate_dict(infodict, infodict['blockdict'])
    readabledict['linkdict'] = iterate_dict(infodict, infodict['linkdict'])        

    # containerdict & templatedict
    target = ['containerdict', 'templatedict']
    for ta in target:
        readabledict[ta] = {}
        for k in infodict[ta].keys():
            itemlabel = infodict['labeldict'][k]
            readabledict[ta][itemlabel] = {}
            readabledict[ta][itemlabel]['blockdict'] = iterate_dict(infodict, infodict[ta][k]['blockdict'])
            readabledict[ta][itemlabel]['linkdict'] = iterate_dict(infodict, infodict[ta][k]['linkdict'])
    
    # groupdict
    readabledict['groupdict'] = {}

    # labeldict
    readabledict['labeldict'] = infodict['labeldict']

    return readabledict

def get_new_uuid():
    my_uuid = uuid.uuid4()
    return str(my_uuid)

def get_new_label(type):
    global tfidx

    newlabel =  '_' + type[0] + str(tfidx[type])
    tfidx[type] += 1

    return newlabel

def get_new_stackid(type):
    global stackidx

    newid = type[0].upper() + str(stackidx[type])
    stackidx[type] += 1

    return newid