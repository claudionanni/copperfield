# Copperfield - MySQL/MariaDB data scrambler

import fileinput
import re
import hashlib
import random

for line in fileinput.input():
    # Replace Names, I keep the first two characters of the identificators for easier reference to original ones
    line = re.sub(r'`(.((?!`).)*)`', lambda x: ''.join([' `',x.group(1)[0:2],hashlib.md5(x.group(1).encode('utf8')).hexdigest()[0:20],'` ']),line.rstrip())
   
    # VARCHAR fields that are too short contain md5 hashes that can collide and this is a problem especially if the field is a key or part of, we replace this with VARCHAR(10), increase if duplicate keys occurr
    line2 = re.sub(r'VARCHAR\((\d)\)',r'VARCHAR(10)' ,line.rstrip(),flags=re.IGNORECASE)

    #line3 = re.sub(r'\'\),',r'\'\),  ', line2.rstrip())

    # Replace Data, I do not touch numbers, and I keep the first two characters of the original string to maintain a minimal ordering.
    # For now we keep the strings at fixed size, 3 + 20, for more realistic testing scenarios it's possible we'll need to to make the len(hash)=len(string)
    line4 = re.sub(r',\'(.((?!((,\')|(\),\())).)*)\'', lambda x: ''.join([",'",x.group(1)[0:3],hashlib.md5(x.group(1).encode('utf8')).hexdigest()[0:20],"'"]),line2.rstrip())
    print(line4)
