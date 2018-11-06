from setuptools import setup, find_packages
import main

# The full version, including alpha/beta/rc tags.

# The short X.Y version.


setup(
    name='DebtsBot',
    version=main.version,
    packages=find_packages(),
    url='https://github.com/mtaranovsky/DebtsBot',
    license='',
    author='Trush',
    author_email='trushboyandriy@gmail.com',
    description='Debts bot for IPS'
)
