#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Pavel Jedlicka <pavel_jedlicka@cz.ibm.com>
# IBM internal usage

# version 0.2 - 2020-02-03 - loading schemas from roles folder, process more schema files
# version 0.1 - 2020-01-15

# Schema_valid action plugin

# action plugin for Ansible 2.x
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleFileNotFound, AnsibleAction, AnsibleActionFail, AnsibleUndefinedVariable
from ansible.module_utils._text import to_bytes, to_text, to_native
from ansible.utils.vars import merge_hash
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from ansible.utils.display import Display
import yaml
import os
from datetime import datetime


display = Display()


class ActionModule(ActionBase):


    def _get_schema_file(self, load_from='files', common_role_name=None, schema_file='schema.yml', tmp=None, task_vars=None):
        """Load schema file from folder files or specific role folder"""
        if common_role_name is None:
            try:
                _schema_file = self._find_needle(load_from, schema_file)
            except AnsibleError as e:
                if task_vars and task_vars.__contains__('role_path'):
                    _schema_file = task_vars['role_path'] + '/' + load_from + '/' + schema_file
                else:
                   raise AnsibleActionFail(to_text(e))
        else:
            if task_vars and task_vars.__contains__('role_path'):
                _schema_file = task_vars['role_path'].replace(task_vars['role_name'], common_role_name) + '/' + load_from + '/' + schema_file
            else:
                raise AnsibleUndefinedVariable("Error, 'role_path' value is missing.")

        try:
            l_schema_file = self._loader.get_real_file(_schema_file)
        except AnsibleFileNotFound as e:
            raise AnsibleFileNotFound("Could not find schema file: %s, %s" % (_schema_file, to_text(e)))

        return _schema_file


    def _append_schema_file(self, schema=None, schema_file=None):
        schema_content = None
        try:
            with open(schema_file) as ysf:
                content = ysf.read()
            schema_content = yaml.safe_load(content)
        except:
            pass

        if schema_content is None:
            display.vvvv(to_text("Nothing to append from schema file %s, is is empty." % to_text(schema_file)))
            return schema

        if schema is None:
            return schema_content
        elif 'properties' in schema and 'properties' in schema_content:
            schema['properties'].update(schema_content['properties'])

        return schema


    def _pretty_yaml(self, content=None):
        return yaml.dump(content, default_flow_style=False)


    def template_variables(self, temp_vars, data_loader, vars_to_template):
        '''Template variables for the schema validation.'''

        # Filter vars to be templated
        vars_to_template = {k: temp_vars[k] for k in vars_to_template}

        # Load templar
        templar = Templar(data_loader, variables=temp_vars)

        try:
            # return merged_hash of temp_vars and templated vars
            temp_vars = merge_hash(
                temp_vars,
                templar.template(vars_to_template, fail_on_undefined=False)
            )

        except Exception as e:
            display.vv(to_text(e))
            pass

        return temp_vars


    def run(self, tmp=None, task_vars=None):

        try:
            import jsonschema
        except Exception as e:
            raise AnsibleError('Unable to import jsonschema for inputs validation. %s' % to_text(e))

        display.vvvv("Starting validation at %s" % datetime.now())

        common_role_name = self._task.args.pop('common_role_name', None)
        schema_file_arg = self._task.args.pop('schema_file', None)
        schema_var_arg = self._task.args.pop('schema_var', None)
        variables = self._task.args.pop('variables', None)
        all_required = self._task.args.pop('all_required', True)

        # Prepare temp_vars for templating
        temp_vars = task_vars.copy()
        data_loader = DataLoader()

        # Load schemas
        schema = None
        schema_files = []

        display.vvvv("Loading schemas at %s" % datetime.now())
        # Load specific files if provided
        if schema_var_arg is not None:
            if schema_var_arg not in temp_vars.keys():
                raise AnsibleActionFail("Error, the schema_var '%s' is not defined." % to_text(schema_var_arg))
            else:
                schema = temp_vars[schema_var_arg]
        else:
            if schema_file_arg is not None:
                schema_files.append(schema_file_arg)
            elif common_role_name is not None:
                schema_files.extend(['config_schema.yml', 'extract_schema.yml'])
            else:
                raise AnsibleActionFail("Error, you cannot specify local schema files and role name at once.")

            for s_file in schema_files:
                temp_schema_file = self._get_schema_file(task_vars=temp_vars, schema_file=s_file, common_role_name=common_role_name)
                schema = self._append_schema_file(schema=schema, schema_file=temp_schema_file)

        display.vvvv("Starting templating at %s" % datetime.now())
        # template variables
        try:
            temp_vars = self.template_variables(temp_vars=temp_vars,
                                                data_loader=data_loader,
                                                vars_to_template=schema['properties'].keys())
        except Exception as e:
            display.vvvv("Error templating: %s" % e)
        display.vvvv("Finished templating at %s" % datetime.now())

        if variables is None:
            try:
                variables = {k: temp_vars[k] for k in schema['properties'].keys()}
            except KeyError as ke:
                if all_required is True:
                    raise AnsibleActionFail("Error, following values are missing or misspelled: %s" % to_text(ke))
                else:
                    pass
        else:
            var_missing = []
            for v in variables.keys():
                if v not in schema['properties'].keys():
                    var_missing.append(v)
            if len(var_missing) != 0:
                raise AnsibleActionFail("Error, following values are missing in the schema: %s" % to_text(var_missing))

        display.vvvv("Starting jsonschema valid at %s" % datetime.now())

        validator = jsonschema.Draft7Validator(schema)

        try:
            validator.check_schema(schema)
        except jsonschema.SchemaError as sch_error:
            raise AnsibleActionFail(to_text(sch_error))

        display.vvvv("Starting iterating variables at %s" % datetime.now())
        try:
            val_errors = validator.iter_errors(variables)
        except Exception as e:
            raise AnsibleActionFail("Unexpected exception during validation: %s" % to_text(e))
        display.vvvv("Finished iterating variables at %s" % datetime.now())

        result = super(ActionModule, self).run(tmp, task_vars)
        result['changed'] = False
        result['failed'] = False
        result['errors'] = []
        result['msg'] = "Variables are valid."

        e_msg = []
        for e in val_errors:
            e_msg.append(list((list(e.schema_path), e.message)))
        if len(e_msg) != 0 and len(e_msg) <= 10:
            result.update(dict(failed=True,
                               errors=e_msg,
                               msg="Variables are NOT valid."))
        elif len(e_msg) > 10:
            display.vv("Validation errors: %s" % to_text(e_msg))
            result.update(dict(failed=True,
                               errors="Too many errors to show ... use verbosity 2.",
                               msg="Variables are NOT valid."))

        return result
