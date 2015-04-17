from django.db import models

class SuperQuerySet(models.QuerySet):

  def iterator(self):
    for obj in super(SuperQuerySet, self).iterator():
      yield obj.actual if hasattr(obj, 'actual') else None

SuperModelManager = models.Manager.from_queryset(SuperQuerySet)
SuperModelManager.use_for_related_fields = True

class SuperModel(models.Model):
  actuals = models.Manager.from_queryset(SuperQuerySet)()
  objects = models.Manager()

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

  class Meta:
    abstract = True

