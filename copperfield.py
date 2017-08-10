# Copperfield - MySQL/MariaDB data scrambler

import fileinput
import re
import hashlib
import random

for line in fileinput.input():
    # Replace Names
    line = re.sub(r'`(.((?!`).)*)`', lambda x: ''.join([' `',x.group(1)[0:2],hashlib.md5(x.group(1).encode('utf8')).hexdigest()[0:20],'` ']),line.rstrip())
   
    # VARCHAR fields that are too short contain md5 hashes that can collide and this is a problem especially if the field is a key or part of, we replace this with VARCHAR(10), increase if duplicate keys occurr
    line2 = re.sub(r'VARCHAR\((\d)\)',r'VARCHAR(10)' ,line.rstrip(),flags=re.IGNORECASE)

    #line3 = re.sub(r'\'\),',r'\'\),  ', line2.rstrip())

    # Replace Data
    line4 = re.sub(r',\'(.((?!((,\')|(\),\())).)*)\'', lambda x: ''.join([",'",x.group(1)[0:3],hashlib.md5(x.group(1).encode('utf8')).hexdigest()[0:20],"'"]),line2.rstrip())
    print(line4)
