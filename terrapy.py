#!/usr/bin/env python

# Copyright 2015,2016 Strigo Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json
import argparse


DESCRIPTION = """
terrapy provides a Pythonic abstraction on top of HashiCorp's Terraform.
It is first aimed at providing a comfortably parsed state and generate
Ansible inventory files from that state, but it also aims to provide an
API to execute terraform commands from Python.
"""


def set_verbose():
    # TODO: This is a very naive implementation. We should really
    # use a logging configuration based on different levels of
    # verbosity.
    # The default level should be something in the middle and
    # different levels of `--verbose` and `--quiet` flags should be
    # supported.
    global verbose
    verbose = True


def is_verbose():
    global verbose
    try:
        return verbose
    except NameError:
        verbose = False
        return verbose


class TerraPyError(Exception):
    pass


def _get_state_files(module_root):
    state_files = []

    for dirpath, _, filenames in os.walk(module_root):
        for name in filenames:
            if os.path.splitext(name)[-1] == '.tfstate':
                state_files.append(os.path.join(dirpath, name))
    # Currently assume there's only one in the root
    return '' if not state_files else state_files[0]


def _get_state_content(tfstate_path):
    with open(tfstate_path) as statefile:
        return json.loads(statefile.read())


def _convert_to_dict(state_filter):
    parsed_filter = {}
    # Handle filter element does not contain =
    for element in state_filter:
        element_type, element_value = element.split('=')
        parsed_filter[element_type] = element_value
    return parsed_filter


def _filter(state, state_filter):
    state_filter = _convert_to_dict(state_filter)
    for module in state['modules']:
        pass


def parse_state(module_root, state_filter):
    state = get_state(module_root)
    filtered_result = _filter(state, state_filter)
    print(json.dumps(filtered_result, indent=4))


def get_state(module_root):
    module_root = module_root or os.getcwd()

    state_file = _get_state_files(module_root)
    if not state_file:
        raise TerraPyError('No statefiles could be found under {0}'.format(
            module_root))

    return _get_state_content(state_file)


def list_modules(module_root):
    state = get_state(module_root)
    modules = set()

    for module in state['modules']:
        modules |= set(module['path'])

    return list(modules)


def list_resources(module_root):
    state = get_state(module_root)
    resources = []

    for module in state['modules']:
        module_name = module['path'][0] if len(module['path']) == \
            1 else module['path'][1]
        for resource in module['resources'].keys():
            resources.append('{0}.{1}'.format(module_name, resource))

    resources.sort()
    return resources


def _prettify_dict(key):
    """Return a human readable format of a key (dict).

    Example:

    Description:   My Wonderful Key
    Uid:           a54d6de1-922a-4998-ad34-cb838646daaa
    Created_At:    2016-09-15T12:42:32
    Metadata:      owner=me;
    Modified_At:   2016-09-15T12:42:32
    Value:         secret_key=my_secret_key;access_key=my_access_key
    Name:          aws
    """
    assert isinstance(key, dict)

    pretty_key = ''
    for key, value in key.items():
        key = key.replace('_', ' ')
        if isinstance(value, dict):
            pretty_value = ''
            for k, v in value.items():
                pretty_value += '{0}={1};'.format(k, v)
            value = pretty_value
        pretty_key += '{0:15}{1}\n'.format(key.title() + ':', value)
    return pretty_key


def _prettify_list(items, title='Items:'):
    """Return a human readable format of a list.

    Example:

    Available Keys:
      - my_first_key
      - my_second_key
    """
    assert isinstance(items, list)

    keys_list = title
    for item in items:
        keys_list += '\n  - {0}'.format(item)
    return keys_list


def _parse_state(args):
    try:
        state = parse_state(args.root, args.FILTER)
        print(state)
    except TerraPyError as ex:
        sys.exit(ex)


def _list_modules(args):
    try:
        state = list_modules(args.root)
        print(_prettify_list(state, 'Modules:'))
    except TerraPyError as ex:
        sys.exit(ex)


def _list_resources(args):
    try:
        state = list_resources(args.root)
        print(_prettify_list(state, 'Resources:'))
    except TerraPyError as ex:
        sys.exit(ex)


def _add_verbose_argument(parser):
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Set verbose logging level')
    return parser


def _set_defaults(parser, func):
    parser = _add_verbose_argument(parser)

    parser.add_argument(
        '-r',
        '--root',
        help='Path to the root module')

    parser.set_defaults(func=func)
    return parser


def _add_modules_command(parser):
    description = ('List all modules')

    command = parser.add_parser(
        'show-modules',
        description=description,
        help='Print out all modules')

    _set_defaults(command, func=_list_modules)
    return parser


def _add_resources_command(parser):
    description = ('List all resources')

    command = parser.add_parser(
        'show-resources',
        description=description,
        help='Print out all resources')

    _set_defaults(command, func=_list_resources)
    return parser


def _add_filter_command(parser):
    description = ('Prints out parsed output')

    command = parser.add_parser(
        'filter',
        description=description,
        help=description)

    command.add_argument(
        'FILTER', nargs='+',
        help='Filter according to which resources will be returned')

    _set_defaults(command, func=_parse_state)
    return parser


# TODO: Find a way to both provide an error handler AND multiple formatter
# classes.
class CustomFormatter(argparse.ArgumentParser):
    def error(self, message):
        # We want to make sure that when there are missing or illegal arguments
        # we error out informatively.
        self.print_help()
        sys.exit('\nerror: %s\n' % message)


def _assert_atleast_one_arg(parser):
    """When simply running `wagon`, this will make sure we exit without
    erroring out.
    """
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit(0)


def parse_args():
    parser = CustomFormatter(
        description=DESCRIPTION,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser = _add_verbose_argument(parser)

    subparsers = parser.add_subparsers()
    subparsers = _add_filter_command(subparsers)
    subparsers = _add_modules_command(subparsers)
    subparsers = _add_resources_command(subparsers)

    _assert_atleast_one_arg(parser)

    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        set_verbose()
    args.func(args)


if __name__ == '__main__':
    main()
