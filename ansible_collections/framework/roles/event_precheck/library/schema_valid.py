#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Pavel Jedlicka <pavel_jedlicka@cz.ibm.com>
# IBM internal usage

# Empty module for schema_valid action plugin

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: schema_valid
version_added: 2.9
short_description: Module for validation of role inputs
description: Module for validation of role input values. Inserted values are validated against json schema using draft7 schema.
options:
  common_role_name:
    description:
      - Name of callable installed local role (that is located in same `roles` folder).
      - If `common_role_name` specified, validation schema is expected to be present
        in two files `roles\{{ common_role_name }}\files\config_schema.yml`
        and `roles\{{ common_role_name }}\files\extract_schema.yml`
      - If any of the schema files is missing, module will fail.
      - Schema files could be empty.
      - If `common_role_name` specified, no other module option is required.

  schema_file:
    description:
      - Names of schema files for validation within the ansible_role_event_validate_input role.
      - Schema files have to be located within role in folder `files`.
      - Required if `common_role_name` is not specified.
      - One or more schema files can be used in a list.
    type: list
    elements: string

  variables:
    description:
        - Addresses all inputs that have to be validated.
        - Respects same structure as expected by schema (use nested arrays or dictionaries as neeed).
        - Only subset of variables for validation can be used.
        - If `variables` not specified, the validation is done againts all variables in current play.
        - Use only for specific custom valiation of specific variables.
    type: object

  all_vars_required:
    description:
      - Validation requires all variables defined in schema file to be defined.
      - Set `all_vars_required` to false if missing variables are allowed.
    type: boolean
    default: True

notes:
    - This is IBM internal module. Results of the module should be evaluated in other task and escalated with respective return code if needed.
author:
    - Pavel Jedlicka
requirements:
    - jsonschema U(https://pypi.org/project/jsonschema/)
'''

EXAMPLES = r'''
- name: Test input variables against role
  schema_valid:
    common_role_name: disk-usage-alert

- name: Test input variables against custom schemas not requiring all vars are defines
  schema_valid:
    schema_file:
      - schema1.yml
      - schema2.yml
    all_vars_required: False

- name: Test input variables against role using custom variables
  schema_valid:
    common_role_name: disk-usage-alert
    variables:
      testint: 123
      teststring: "123"
      testbool: False
      array:
        - value1
        - value2
      dict:
        var1: var
        var2: var

- name: Test input variables against custom schemas using custom variables
  schema_valid:
    schema_file:
      - schema1.yml
      - schema2.yml
    variables:
      testint: 123
      teststring: "123"
      testbool: False
      array:
        - value1
        - value2
      dict:
        var1: var
        var2: var
'''

RETURN = r'''
msg:
  description: Message that holds output of discrepancies when any variable not valid
  returned: always
  type: str
  sample: [[[\'properties\', \'site_port\', \'type\'], \"\'80f\' is not of type \'integer\'\"]]
'''
