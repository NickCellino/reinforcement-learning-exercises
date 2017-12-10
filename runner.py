import sys, runpy
import os.path

sys.path.append(os.path.dirname(__file__))

executable = sys.argv[1]
sys.argv = sys.argv[1:]

runpy.run_path(executable)
