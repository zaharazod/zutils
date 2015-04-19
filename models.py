import os
from django.db.models import Max
from random import randint
from django.template import Template, Context
from django.template.loader import get_template
from django.db import models

# SuperModel: querying the default manager (actuals) will return subclassed instances of this model
class SuperQuerySet(models.QuerySet):
  def iterator(self):
    for obj in super(SuperQuerySet, self).iterator():
      yield obj.actual if hasattr(obj, 'actual') else None

SuperModelManager = models.Manager.from_queryset(SuperQuerySet)
SuperModelManager.use_for_related_fields = True

class SuperModel(models.Model):
  actuals = models.Manager.from_queryset(SuperQuerySet)()

  @property
  def actual(self):
    if hasattr(self, '_actual'): return self._actual
    for name in [ model._meta.model_name
                  for model in models.get_models()
                  if issubclass(model, self.__class__) ]:
      try:
        self._actual = getattr(self, name)
        return self._actual
      except: pass
    return self

  class Meta: abstract = True

# RandomModel: 
class RandomQuerySet(models.QuerySet):
  def random(self):
    if not hasattr(self, '_random_generator'):
      self._random_generator = self._random()
    return self._random_generator.next()

  def _random(self, limit=1000):
   max_ = self.model._default_manager.aggregate(Max('id'))['id__max']
   i = 0
   while i < limit:
       try:
           yield self.model._default_manager.get(pk=randint(1, max_))
           #i += 1
       except self.model.DoesNotExist:
           pass

RandomModelManager = models.Manager.from_queryset(RandomQuerySet)
RandomModelManager.use_for_related_fields = True

class RandomModel(models.Model):
  random = RandomModelManager()
  class Meta: abstract = True

# DisplayModel: shortcut methods to render object with a template
class DisplayModel(models.Model):
  def get_template_prefix(self): return None
  def get_template_ext(self): return None

  def get_template_name(self, ext=None):
    tmplname = self._meta.model_name
    tmplprefix = self.get_template_prefix()
    tmplext = ext or self.get_template_ext() or 'html'
    if tmplprefix: tmplname = tmplprefix + '_' + tmplname
    tmplname = self._meta.app_label + '/' + tmplname + '.' + tmplext
    return tmplname

  def display(self, ext=None):
    tmpl = get_template(self.get_template_name())
    ctx = Context({'obj' : self})
    return tmpl.render(ctx)

  class Meta: abstract = True

class ZUtilQuerySet(SuperQuerySet, RandomQuerySet): pass
ZUtilManager = models.Manager.from_queryset(ZUtilQuerySet)
ZUtilManager.use_for_related_fields = True

class ZUtilBase(models.Model):
  objects = models.Manager()
  class Meta: abstract = True

class ZUtilModel(ZUtilBase, SuperModel, RandomModel, DisplayModel):
  objectz = ZUtilManager()
  class Meta: abstract = True
