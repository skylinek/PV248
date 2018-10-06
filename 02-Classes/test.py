import sys
import re
from scorelib import *

if len(sys.argv)!=2:
    print("Wrong Number Arguments")
    raise SystemExit

filename = sys.argv[1]
prints=load(filename)

for OnePrint in prints:
    OnePrint.format()
    print()