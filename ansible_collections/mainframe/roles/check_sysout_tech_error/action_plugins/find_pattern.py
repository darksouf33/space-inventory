#!/usr/bin/python
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleFileNotFound, AnsibleAction, AnsibleActionFail, AnsibleUndefinedVariable
from ansible.utils.display import Display
from datetime import datetime

display = Display()


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        display.v("Starting validation at %s" % datetime.now())

        if task_vars is None:
            task_vars = dict()

        # Check errors data to check are present
        errors_var = self._task.args.pop('sysout_errors_to_find', None)
        if errors_var is None:
            raise AnsibleActionFail(
                "La variable sysout_errors_to_find doit être renseignée")

        sysout_var = self._task.args.pop('sysout_to_check', None)
        if sysout_var is None:
            raise AnsibleActionFail(
                "La variable sysout_to_check doit être renseignée")

        display.vvv("errors_var : %s" % errors_var)
        display.vvv("sysout_var : %s" % sysout_var)

        # Init result vars
        sysout_tech_error_found = False
        sysout_tech_error_line = ''

        # Check if a pattern is found in the sysout var
        for pattern in errors_var:
            display.v("Try pattern : %s" % pattern)
            if pattern and pattern in sysout_var:
                sysout_tech_error_found = True
                display.v("Found")

                # Find the line where error msg appears
                for line in sysout_var.split('\n'):
                    if pattern in line:
                        sysout_tech_error_line = line
                        break
                break

        ret = dict()
        ret['sysout_tech_error_found'] = sysout_tech_error_found
        ret['sysout_tech_error_line'] = sysout_tech_error_line

        return dict(ansible_facts=dict(ret))
