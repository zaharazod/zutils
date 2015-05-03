from collections import namedtuple
from django.db import models
from django.core.exceptions import ValidationError

from django.utils.six import with_metaclass, string_types

Choice = namedtuple('Choice', ('value', 'display', 'slug', 'handler',))

class ChoiceField(with_metaclass(models.SubfieldBase, models.PositiveSmallIntegerField)):
  description = 'Integer-backed choice field'
  def __init__(self, options, *args, **kwargs):
    self._options = options
    kwargs['choices'] = [ (x.value, x.display) for x in options ]
    super(ChoiceField, self).__init__(*args, **kwargs)

  def  deconstruct(self):
    name, path, args, kwargs = super(ChoiceField, self).deconstruct()
    kwargs['options'] = self._options
    return name, path, args, kwargs

  def to_python(self, value):
    if isinstance(value, Choice) and value in self._options:
      return value
    for c in self._options:
      if value in c: return c
    raise ValidationError('invalid choice')

  def get_prep_value(self, value):
    return value.value

