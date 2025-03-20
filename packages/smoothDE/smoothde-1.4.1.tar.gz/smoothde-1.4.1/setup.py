from setuptools import setup
from pathlib import Path 
import os
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()
setup(
    name='smoothDE',
    version='1.4.1',
    description='This package uses smoothing to create a density estimate',
    url='https://github.com/rhys-m-adams/smoothDE',
    author='Rhys M. Adams',
    author_email='rhys.adams@protonmail.com',
    license='MIT',
    long_description=long_description, 
    long_description_content_type='text/markdown',
    packages=['smoothDE'],
    install_requires=[
                'scikit-sparse',
                'numpy',
                'scipy',
                'scikit-learn',
            ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
)
