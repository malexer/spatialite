from setuptools import setup
from codecs import open
from os import path


cwd = path.abspath(path.dirname(__file__))


with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spatialite',
    version='0.0.1',

    description='Wrapper of sqlite3 module which adds SpatiaLite support.',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
