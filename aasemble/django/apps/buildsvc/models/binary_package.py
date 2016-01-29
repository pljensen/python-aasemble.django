from django.db import models

from aasemble.django.apps.buildsvc.models.repository import Repository


BINARY_PACKAGE_TYPE_DEB = 1
BINARY_PACKAGE_TYPE_UDEB = 2
BINARY_PACKAGE_TYPE_DDEB = 3
BINARY_PACKAGE_TYPE_CHOICES = ((BINARY_PACKAGE_TYPE_DEB, 'Debian package (.deb)'),
                               (BINARY_PACKAGE_TYPE_UDEB, 'Debian-installer package (.udeb)'),
                               (BINARY_PACKAGE_TYPE_DDEB, 'Debug Debian package (.ddeb)'))


class BinaryPackage(models.Model):
    name = models.CharField(max_length=200)
    repository = models.ForeignKey(Repository)

    def __str__(self):
        return '%s' % (self.name,)

    class Meta:
        unique_together = (('name', 'repository'),)
