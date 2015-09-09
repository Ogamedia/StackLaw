# It's an update of snippet https://djangosnippets.org/snippets/1376/ to work with Django 1.8. 
# With this piece of code, you can override admin templates without copy or symlink files. 
# Just write your template and extend the target.

import io
from os.path import dirname, join, abspath
from django.db.models import get_app
from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader

from django import template
register = template.Library()


class Loader(BaseLoader):
    is_usable = True

    def get_template_path(self, app_template_name, template_dirs=None):
        template_parts = app_template_name.split(":", 1)

        if len(template_parts) != 2:
            raise TemplateDoesNotExist()

        app_name, template_name = template_parts
        app_dir = dirname(get_app(app_name).__file__)
        template_dir = abspath(join(app_dir, 'templates'))

        return join(template_dir, template_name)

    def load_template_source(self, template_name, template_dirs=None):
        filepath = self.get_template_path(template_name, template_dirs)
        try:
            with io.open(filepath, encoding=self.engine.file_charset) as fp:
                return fp.read(), filepath
        except IOError:
            pass
        raise TemplateDoesNotExist(template_name)