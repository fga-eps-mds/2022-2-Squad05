import os, pathlib,sys
import pytest


os.chdir('tests/')
sys.path.append(os.path.abspath('../src/'))

pytest.main()