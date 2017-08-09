# Copperfield - MySQL/MariaDB data scrambler

import fileinput
import re
import hashlib
import random

for line in fileinput.input():
    line = re.sub(r'`.((?!`).)*`', lambda x: ''.join([' `',hashlib.md5(x.group().encode('utf8')).hexdigest(),'` ']),line.rstrip())
    line4 = re.sub(r',\'.((?!,\').)*\'', lambda x: ''.join([",'",hashlib.md5(x.group().encode('utf8')).hexdigest()[0:40],"'"]),line.rstrip())
    print(line4)
