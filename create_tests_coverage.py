import os, pathlib,sys
import pytest
import pytest_cov

os.chdir('tests/')

sys.path.append(os.path.abspath('../src/'))

pytest.main(["--cov-report","term:skip-covered","--cov-report","xml:../coverage.xml","--cov=../src/"])

os.chdir('../')

print(os.listdir('./'))
