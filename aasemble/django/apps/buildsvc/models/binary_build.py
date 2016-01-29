from django.db import models

from aasemble.django.apps.buildsvc.models.architecture import Architecture
from aasemble.django.apps.buildsvc.models.source_package_version import SourcePackageVersion


class BinaryBuild(models.Model):
    source_package_version = models.ForeignKey(SourcePackageVersion)
    architecture = models.ForeignKey(Architecture)

    def __str__(self):
        return '%s_%s' % (self.source_package_version, self.architecture)
