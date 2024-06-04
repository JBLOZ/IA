import numpy as np

import excepcions as ex
import csv
import pickle
import json
import os
import shutil
import numpy as np
import re

def search(cadena):

    search1 = re.match(r'(/n{1,3})', cadena)
    search2 = re.match(r'(?=.*[0-9])', cadena)


    return search1, search2



if __name__ == '__main__':
    print(search('ho9a/n/n/n'))
