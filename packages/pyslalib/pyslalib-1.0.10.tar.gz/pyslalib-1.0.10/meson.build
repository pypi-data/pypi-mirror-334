project(
    'slalib',
    ['c', 'fortran'],
    version : '1.0.10',
    meson_version: '>= 1.1.0',
    default_options: [
        'warning_level=1',
        'buildtype=release',
    ]
)

add_project_arguments('-DNPY_NO_DEPRECATED_API=0', language : 'c')
add_project_arguments('-DNPY_TARGET_VERSION=NPY_1_23_API_VERSION', language : 'c')

py = import('python').find_installation('python3', pure: false)
py_dep = py.dependency()

incdir_numpy = run_command(
    py, ['-c', 'import numpy; print(numpy.get_include())'], check : true
).stdout().strip()

incdir_f2py = run_command(
    py, ['-c', 'import numpy.f2py; print(numpy.f2py.get_include())'], check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy)
np_dep = declare_dependency(include_directories: inc_np)

incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'
inc_f2py = include_directories(incdir_f2py)
fortranobject_c = incdir_f2py / 'fortranobject.c'

inc_np = include_directories(incdir_numpy, incdir_f2py)
# gh-25000
fc = meson.get_compiler('fortran')
quadmath_dep = fc.find_library('quadmath', required: false)

run_command(
    py, ['-m', 'numpy.f2py', 'slalib.pyf', '*.f', '*.F', '*.h'], check : true
).stdout().strip()

slalib_sources = []
foreach suff: ['f', 'F']
    slalib_sources += run_command(
        py,
        ['-c', 'from glob import glob; print("\\n".join(glob("*.' + suff + '")), end="")'],
        check: true).stdout().split('\n')
endforeach
slalib_sources += ['slalibmodule.c', fortranobject_c]

run_command(
    py, ['-c', '''
import sys, pickle
sys.path.insert(0, ".")
from get_docstring import get_docstring
with open("pyslalib/docstring_pickle.pkl", "wb") as f:
    pickle.dump(get_docstring(), f)
'''], check : true
)

py.install_sources(['pyslalib' / '__init__.py', 'pyslalib' / 'docstring_pickle.pkl'], subdir: 'pyslalib')

py.extension_module(
    'slalib',
    sources: slalib_sources,
    include_directories: [inc_np],
    dependencies: [py_dep, quadmath_dep],
    install : true,
    subdir: 'pyslalib',
)
