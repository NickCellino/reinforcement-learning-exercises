import sys, runpy
import os.path

sys.path.append(os.path.dirname(__file__))

module = sys.argv[1]
sys.argv = sys.argv[1:]

runpy.run_module(module)
