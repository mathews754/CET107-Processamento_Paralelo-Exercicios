from setuptools import setup
from Cython.Build import cythonize

# Comando para fazer o setup
# python3 setup.py build_ext --inplace

setup(
    name='vid_limiarizacao',
    ext_modules=cythonize("limiar.pyx"),
    zip_safe=False,
)