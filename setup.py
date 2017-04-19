import os
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='terrapy',
    version="0.1.0",
    url='https://github.com/strigo/terrapy',
    author='strigo',
    author_email='ops@strigo.io',
    license='LICENSE',
    platforms='All',
    description="terrapy proides a Pythonic abstraction on HashiCorp's Terraform",  # NOQA
    long_description=read('README.rst'),
    py_modules=['terrapy'],
    entry_points={'console_scripts': ['terrapy = terrapy:main']},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
