#!/usr/bin/python3
#  OpenVPN 3 Linux client -- Next generation OpenVPN client
#
#  Copyright (C) 2017 - 2020  OpenVPN Inc. <sales@openvpn.net>
#  Copyright (C) 2017 - 2020  David Sommerseth <davids@openvpn.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, version 3 of the
#  License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

##
# @file  gen-openvpn2-completion.py
#
# @brief  Generates a static openvpn2 bash-completion helper script
#         based on the arguments the openvpn3 python module supports
#

import sys
import argparse
from jinja2 import Template

completion_template = """#  OpenVPN 3 Linux client -- Next generation OpenVPN client
#
#  Copyright (C) 2020         OpenVPN Inc. <sales@openvpn.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, version 3 of the
#  License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#  This script is automatically generated by gen-openvpn2-completion.py
#  Any modifications here will be overwritten.
#

_openvpn2_completion()
{
    local cur prev OPTS
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    case $prev in
    {% for option, values in valid_args.items() %}
        '{{ option }}')
            COMPREPLY=( $(compgen -W  "{{ values }}" -- $cur) )
            return 0
            ;;
    {% endfor %}
    esac
    case $cur in
        -*)
            OPTS="{{ option_list }}"
            COMPREPLY=( $(compgen -W "${OPTS[*]}" -- $cur) )
            return 0;
            ;;
    esac
    return 0
}

complete -F _openvpn2_completion openvpn2
"""


if __name__ == '__main__':
    argp = argparse.ArgumentParser(description='Generate openvpn2 bash-completion helper')
    argp.add_argument('--python-source-dir', action='store', required=True)
    args = argp.parse_args()

    if None == args.python_source_dir:
        print("The --python-source-dir option is required")
        sys.exit(2)

    # Configure a dummy OpenVPN 3 ConfigParser, so the
    # supported options and arguments can be extracted
    sys.path.insert(0, args.python_source_dir)
    import openvpn3
    cfgparser = openvpn3.ConfigParser([sys.argv[0],], argp.description)
    completion_data = cfgparser.RetrieveShellCompletionData()

    # Generate the bash-completion script
    valid_args = {}
    for opt, values in completion_data['argvalues'].items():
        if len(values) > 1:
            valid_args[opt] = '{' + ','.join(['"%s"' % v for v in values]) + '}'
        else:
            valid_args[opt] = '%s' % values[0]

    option_list = '{' + ','.join(['"%s"' % o for o in completion_data['options']]) + '}'

    ctpl = Template(completion_template)
    script = ctpl.render(valid_args=valid_args, option_list=option_list)

    print(script)