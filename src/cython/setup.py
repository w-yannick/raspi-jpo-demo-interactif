from distutils.core import setup
from Cython.Build import cythonize

setup(name="optimizedFilter", ext_modules=cythonize('optimizedFilter.pyx'),)
