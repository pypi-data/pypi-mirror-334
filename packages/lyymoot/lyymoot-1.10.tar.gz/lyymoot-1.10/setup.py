from setuptools import setup

setup(
    name='lyymoot',
    version='1.10',
    author='yy',
    author_email='',
    description='lyymoot for lyy',
    #packages=find_packages(),
    packages=['lyymoot'], 
    package_dir={'lyymoot': '.'},
    py_modules=['lyymoot','utils','quotes','consts'],
    license="MIT",
    install_requires=[
    ],
)
