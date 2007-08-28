import doctest
import sys

doctest.testfile(sys.argv[1], report=True, verbose=True)