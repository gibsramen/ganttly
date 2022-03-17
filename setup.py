# Much of this page is taken from the gemelli setup file
import ast
import re
from setuptools import find_packages, setup

# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("ganttly/__init__.py", "rb") as f:
    hit = _version_re.search(f.read().decode("utf-8")).group(1)
    version = str(ast.literal_eval(hit))

setup(
    name="ganttly",
    version=version,
    author="Gibraan Rahman",
    author_email="gibsramen@gmail.com",
    packages=find_packages()
)
