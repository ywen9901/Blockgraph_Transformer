# Global var for apis

from .example import infodict

global tfidx
tfidx = {'block': 8, 'port': 9, 'link': 5, 'slot': 13, 'group': 0}

global stackidx, designdict, stackdict, curstack, stackloc
stackidx = {'stack': 1, 'design': 1}
designdict = {'D0': infodict['design']}
stackdict = {'S0': ['D0']}
curstack = 'S0'
stackloc = {'S0': 'D0'}