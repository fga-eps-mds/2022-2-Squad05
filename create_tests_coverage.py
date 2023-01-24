import os, pathlib,sys
import pytest
import pytest_cov

os.chdir('tests/')

sys.path.append(os.path.abspath('../src/'))

pytest.main(["--junitxml=../pytest.xml","--cov-report","term:skip-covered","--cov=../src/"])

os.chdir('../')

print(os.listdir('./'))

''