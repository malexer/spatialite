from setuptools import setup
from codecs import open
from os import path


cwd = path.abspath(path.dirname(__file__))


def get_long_description():
    with open(path.join(cwd, 'README.rst'), encoding='utf-8') as f:
        return f.read()


def get_version():
    exec_locals = {}
    with open(path.join(cwd, 'spatialite', 'version.py')) as f:
        exec(f.read(), {}, exec_locals)
    return exec_locals['__version__']


setup(
    name='spatialite',
    version=get_version(),

    description='Wrapper of sqlite3 module which adds SpatiaLite support.',
    long_description=get_long_description(),
    url='https://github.com/malexer/spatialite',

    author='Alex (Oleksii) Markov',
    author_email='alex@markovs.me',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords=('sqlite sqlite3 spatialite'),

    packages=['spatialite'],
)
