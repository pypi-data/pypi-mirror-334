from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os

class get_pybind_include:
    """Helper class to determine the pybind11 include path"""
    def __str__(self):
        import pybind11
        return pybind11.get_include()

ext_modules = [
    Extension(
        'cosbr.gcp_module',  # Note the change to cosbr.gcp_module
        ['cosbr/gcp_bindings.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
        ],
        language='c++',
        extra_compile_args=['-std=c++11'],
    ),
]

# Read the README for the long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cosbr',
    version='0.1.0',
    description='Solver using Simulated Bifurcation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/cosbr',
    packages=['cosbr'],
    ext_modules=ext_modules,
    setup_requires=['pybind11>=2.5.0'],
    install_requires=['pybind11>=2.5.0', 'numpy'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
)