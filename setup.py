from setuptools import setup, find_packages
import sys
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version():
    with open(os.path.join('aeternity', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')

long_description = None
if 'upload' in sys.argv or 'register' in sys.argv:
    readmemd = "\n" + "\n".join([read('README.md')])
    print("converting markdown to reStucturedText for upload to pypi.")
    from urllib.request import urlopen
    from urllib.parse import quote
    import json
    import codecs
    url = 'http://pandoc.org/cgi-bin/trypandoc?from=markdown&to=rst&text=%s'
    urlhandler = urlopen(url % quote(readmemd))
    result = json.loads(codecs.decode(urlhandler.read(), 'utf-8'))
    long_description = result['html']
else:
    long_description = "\n" + "\n".join([read('README.md')])

setup(
    name='aeternity',
    version=get_version(),
    description='Perform actions on the aeternity block chain',
    long_description=long_description,
    author='Tom Wallroth',
    author_email='tomwallroth@gmail.com',
    url='https://github.com/devsnd/aeternity/',
    license='ISC',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
    tests_require=["nose"],
)
