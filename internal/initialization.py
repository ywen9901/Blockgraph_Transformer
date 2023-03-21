from ..setup import tfidx, scripts

def get_new_id(type):
    newid =  '_' + type[0] + str(tfidx[type])
    tfidx[type] += 1

    scripts.append('get_new_id')
    return newid

def set_design(infodict): ##### test all functions!!!!!
    # Need to parse JSON to Python dictionary
    scripts = []

    UIaction = infodict['action']
    target = infodict['target']
    blockdict = infodict['design']['blockdict']
    linkdict = infodict['design']['linkdict']
    containerdict = infodict['design']['containerdict']
    groupdict = infodict['design']['groupdict']

    eval(UIaction)(blockdict, linkdict, containerdict, groupdict, target)