from setuptools import setup, find_packages

VERSION = '0.3.0' 
DESCRIPTION = 'The MADCUBA python package.'

# Setting up
setup(
    name="madcubapy", 
    version=VERSION,
    author="David Haasler García",
    author_email="dhaasler@cab.inta-csic.es",
    description=DESCRIPTION,
    long_description=open('PYPIREADME.rst', 'r').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/dhaasler/madcubapy',
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "astropy>=6.0.0",
        "matplotlib>=3.6.0",
        "numpy>=1.23.0",
        "scipy>=1.9.2"
    ],
    keywords=[
        'madcuba',
        'radio astronomy',
    ],
    classifiers= [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
