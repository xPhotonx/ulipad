import doctest
import os, sys

execfile(sys.argv[1])
doctest.testmod(report=True, verbose=True)
