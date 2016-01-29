from django.db import models

from aasemble.django.apps.buildsvc.models.repository import Repository


class SourcePackage(models.Model):
    name = models.CharField(max_length=200)
    repository = models.ForeignKey(Repository)

    def __str__(self):
        return '%s' % (self.name,)

    class Meta:
        unique_together = (('name', 'repository'),)