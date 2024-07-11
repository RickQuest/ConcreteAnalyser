import os
from setuptools import setup, find_packages

# set version
VERSION = '0.2.6'
LONG_DESCRIPTION = ''

# setup(
#     name="concreteanalyser",
#     install_requires=[
#         # "colorama; platform_system == 'Windows'",
#         "importlib-metadata; python_version < '3.8'",
#     ],
# )
def get_requirements():
    """Loads contents from requirements.txt."""
    requirements = []
    with open('requirements.txt') as f:
        data = f.read().splitlines()
    if any(data):
        data = data[1:]
        requirements = [item.split(";")[0].split(" ")[0] for item in data]
    return requirements

# with open('README.rst') as fobj:
#     LONG_DESCRIPTION = fobj.read()

setup(
    name='concreteanalyser',
    version=VERSION,
    author='Eric Surprenant',
    url='https://github.com/Eric-Surprenant/ConcreteAnalyser',
    # download_url='https://github.com/Eric-Surprenant/ConcreteAnalyser/archive/' + VERSION + '.tar.gz',
    description="Concrete air void system analyser software",
    # long_description=LONG_DESCRIPTION,
    license='MIT License',
    platforms='any',
    packages=find_packages(exclude=['.vscode',
                                    'archive',
                                    'conda',
                                    'latex',
                                    'labeling',
                                    'matlab',
                                    'old',
                                    'tests']),
    install_requires=['opencv-python','matplotlib','scipy','numpy','imutils','pillow','pyserial'],
    include_package_data=True,
)