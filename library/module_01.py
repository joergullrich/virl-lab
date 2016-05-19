#!/usr/bin/env python
#

DOCUMENTATION = '''
---

module: module_01
short_description: testmodul, sollen mal eigene module werden
description:
    - Offers foo
author: Joerg Ullrich
options:
    bla:
        description:
            - location where tests are located
        required: true
        default: null
        choices: []
        aliases: []
'''

EXAMPLES = '''
- module_01:

'''

from os import walk
from ansible.utils import module_docs


def main():

    module = AnsibleModule(
        argument_spec=dict(
            path=dict(default='tests'),
        ),
        supports_check_mode=False
    )

    path = module.params['path']

    if path[-1] != '/':
        path = path + '/'

    tests = []
    for (dirpath, dirnames, files) in walk(path):

    module.exit_json(tests=tests)


from ansible.module_utils.basic import *
main()
