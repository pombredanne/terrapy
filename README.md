terrapy
=======

[![Travis Build Status](https://travis-ci.org/nir0s/ghost.svg?branch=master)](https://travis-ci.org/nir0s/ghost)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/kuf0x8j62kts1bpg/branch/master?svg=true)](https://ci.appveyor.com/project/nir0s/ghost)
[![PyPI Version](http://img.shields.io/pypi/v/ghost.svg)](http://img.shields.io/pypi/v/ghost.svg)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/ghost.svg)](https://img.shields.io/pypi/pyversions/ghost.svg)
[![Requirements Status](https://requires.io/github/nir0s/ghost/requirements.svg?branch=master)](https://requires.io/github/nir0s/ghost/requirements/?branch=master)
[![Code Coverage](https://codecov.io/github/nir0s/ghost/coverage.svg?branch=master)](https://codecov.io/github/nir0s/ghost?branch=master)
[![Code Quality](https://landscape.io/github/nir0s/ghost/master/landscape.svg?style=flat)](https://landscape.io/github/nir0s/ghost)
[![Is Wheel](https://img.shields.io/pypi/wheel/ghost.svg?style=flat)](https://pypi.python.org/pypi/ghost)

`terrapy` is a Pythonic abstraction above HashiCorp's Terraform.


## Alternatives

* While [Vault](http://vaultproject.io) is truly spectacular and I've been using it for quite a while now, it requires a server running.


## Installation

terrapy supports Linux on Python 2.7 and 3.3+

```shell
pip install terrapython
```

For dev:

```shell
pip install https://github.com/strigo/terrapy/archive/master.tar.gz
```


## Usage

### CLI

```shell
$ terrapy parse terraform.tfstate
$ terrapy generate ansible-inventory terraform.tfstate --format=ini
...

```


## Testing

```shell
git clone git@github.com:strigo/terrapy.git
cd terrapy
pip install tox
tox
```


## Contributions..

See [CONTRIBUTIONS](https://github.com/strigo/terrapy/blob/master/CONTRIBUTING.md)
on how to contribute.

Pull requests are always welcome..
