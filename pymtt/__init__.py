#!/usr/bin/env python
import imp
import os
import sys
from optparse import OptionParser

from jinja2 import Environment, FileSystemLoader


class PyMTT(object):
    ALLOWED_TYPES = (int, float, basestring, tuple, list, dict)

    def __init__(self, template_dir):
        '''Create config generator.

        template_dir: filesystem path to search for templates.
        '''
        self.output_dir = os.path.abspath(template_dir)
        self.context = {}
        loader = FileSystemLoader(self.output_dir)
        self.env = Environment(loader=loader, extensions=['jinja2.ext.with_'],
                               trim_blocks=True)

    def update_context_from_module(self, module):
        '''Update current context from module.

        Updates context with attributes from the given module.
        Attributes which start with underscore are ignored.

        module: module object.
        '''
        for attr in dir(module):
            if attr.startswith('_'):
                continue
            val = getattr(module, attr)
            if any(isinstance(val, tp) for tp in self.ALLOWED_TYPES):
                self.context[attr] = val


    def update_context_from_modules(self, modules):
        '''Update current context from modules.

        Updates context with attributes from the given modules.
        Each module overwrites attributes of the current context.

        modules: iterable of module objects.
        '''
        for module in modules:
            self.update_context_from_module(module)

    def update_context_from_env(self):
        '''Update current context from environment.'''
        for attr, value in os.environ.iteritems():
            try:
                value = eval(value)
            except:
                pass
            self.context[attr] = value

    def module_from_file(self, filename):
        '''Import module from file.

        filename: module path.
        '''
        return imp.load_source(filename, filename)

    def modules_from_files(self, filenames):
        '''Import modules from files.

        filenames: iterable of modules' paths.
        '''
        return map(self.module_from_file, filenames)

    def render(self, template_name):
        '''Render template using current context.

        template_name: name of the template.
        '''
        template = self.env.get_template(template_name)
        return template.render(self.context)

    def render_and_write(self, template_name, output):
        '''Render template using context and save it to file.

        template_name: name of the template.
        context: context dict.
        output: output file name or path.
        '''
        output_dir = os.path.dirname(output)
        if output_dir:
            output_dir = os.path.abspath(output_dir)
        else:
            output_dir = self.output_dir
        output_file = os.path.join(output_dir, os.path.basename(output))
        with open(output_file, 'w') as f:
            f.write(self.render(template_name))
