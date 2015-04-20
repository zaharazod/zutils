import os
from django.template import Library, Template, Context
from django.template.loader import get_template

register = Library()

@register.simple_tag(takes_context=True)
def embed(context, obj, prefix=None):
    tmplname = obj._meta.model_name + '.html'
    if prefix is not None: tmplname = prefix + '_' + tmplname
    tmplname = os.path.join(obj._meta.app_label, tmplname)
    tmpl = get_template(tmplname)
    c = Context({'obj':obj})
    return tmpl.render(c)
