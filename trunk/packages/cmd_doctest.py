import doctest
import sys

print sys.argv[1]
doctest.testfile(sys.argv[1], report=True, verbose=True)