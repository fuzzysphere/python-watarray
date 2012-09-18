from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    cython_available = False
else:
    cython_available = True

cmdclass = {}

if cython_available:
    files = ["watarray.pyx", "io.cpp"]
    cmdclass['build_ext'] = build_ext
else:
    files = ["watarray.cpp", "io.cpp"]

ext_modules = [Extension(
    "watarray",
    files,
    language="c++",
    include_dirs=["."],
    libraries=["wat_array"],
)]

setup(
    name='python-watarray',
    version='0.6dev',
    description='python wrappers for wat-array, a wavelet tree library',
    author='fuzzysphere',
    url='https://github.com/fuzzysphere/python-watarray',
    license='MIT',
    ext_modules=ext_modules,
    cmdclass=cmdclass,
)
