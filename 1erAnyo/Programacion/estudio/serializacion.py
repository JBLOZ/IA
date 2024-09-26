import os
import json
import re
import pickle



class Password:

    def __init__(self, passw):

        if self.comprobarpassw(passw) == 0:

            self._password = passw


def comprobarpassw(passw):

    if len(passw) < 8:
        return 1
    elif not re.search('[A-Z]', passw):
        return 2
    elif not re.search('[a-z]', passw):
        return 3
    elif not re.search('[0-9]', passw):
        return 4
    elif not re.search('[!@#$%^&*()]', passw):
        return 5
    elif re.search('[A-Z]{3}|[a-b]{3}|[0-9]{3}',passw):
        return 6
    else:
        return 0





print(comprobarpassw('23k3sKK((j'))