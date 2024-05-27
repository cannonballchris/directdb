from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.6'
DESCRIPTION = 'An async package that makes database handling extremely easy!'

# Setting up
setup(
    name="directdb",
    version=VERSION,
    author="Cannonball Chris",
    author_email="cannonballchris8@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['asyncpg', 'aiosqlite'],
    keywords=['db', 'bot', 'discord bot', 'database', 'postgresql', 'asyncpg', 'async', 'pgutils', 'nosql', 'sqlite', 'aiosqlite', 'discord.py'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

