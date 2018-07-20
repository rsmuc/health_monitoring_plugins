import os
import sys

tests_dir = os.path.dirname( os.path.abspath(__file__) )
package_path = os.path.join(tests_dir, '..')
sys.path.insert(0, package_path)
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
os.environ['PYTHONPATH'] = package_path
testenv = os.environ
