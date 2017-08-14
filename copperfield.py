### MASTER

# Copperfield v.0.1 - MySQL/MariaDB data scrambler                      (c)2017 Claudio Nanni

# It scrambles data in a mysqldump output so that data is not recognizable, useful to protect sensitive data when it must be shared for testing/debugging purposes
# Scrambling data has limitations when bugs are related to a specific string or character, we try to keep a minimal of alphabetic ordering, numbers are not touched
# Also identificators(object names) are scrambled

import fileinput
import re
import hashlib
import random

for line in fileinput.input():

    # Remove Host and Database
    line = re.sub(r'^-- Host. \d+.\d+.\d+.\d+ +Database: .*','-- Host: xxx.xxx.xxx.xxx     Database: XXXXXXXX',line.rstrip())

    # Replace Names, I keep the first two characters of the identifiers for easier reference to original ones. As identifiers are less numerous than data I can pretend 10 characters only of the md5 hash are enough to avoid collisions.
    line = re.sub(r'`(.((?!`).)*)`', lambda x: ''.join(['`',x.group(1)[0:2],hashlib.md5(x.group(1).encode('utf8')).hexdigest()[0:10],'`']),line.rstrip())
   
    # VARCHAR fields that are too short contain md5 hashes that can collide and this is a problem especially if the field is a key or part of, we replace this with VARCHAR(10), increase if duplicate keys occurr
    line2 = re.sub(r'VARCHAR\((\d)\)',r'VARCHAR(10)' ,line.rstrip(),flags=re.IGNORECASE)

    #line3 = re.sub(r'\'\),',r'\'\),  ', line2.rstrip())

    # Replace Data, I do not touch numbers, and I keep the first two characters of the original string to maintain a minimal ordering.
    # For now we keep the strings at fixed size, 3 + 21, for more realistic testing scenarios it's possible we'll need to to make the len(hash)=len(string)
    # I assume that 21 characters of the md5 hash are enough to avoid collisions, if it's not the case with a specific dataset, increase it.
    line4 = re.sub(r',\'(.((?!((,\')|(\),\())).)*)\'', lambda x: ''.join([",'",x.group(1)[0:3],hashlib.md5(x.group(1).encode('utf8')).hexdigest()[0:21],"'"]),line2.rstrip())
    print(line4)
