from setuptools import setup, find_packages

setup(
    name='cm_msh',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
      'gmsh',
      'numpy',
      'matplotlib',
    ],
)