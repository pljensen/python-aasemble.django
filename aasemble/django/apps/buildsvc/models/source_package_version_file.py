from django.db import models

from aasemble.django.apps.buildsvc.models.source_package_version import SourcePackageVersion


SOURCE_PACKAGE_FILE_TYPE_DSC = 1
SOURCE_PACKAGE_FILE_TYPE_ORIG_TARBALL = 2
SOURCE_PACKAGE_FILE_TYPE_DIFF = 3
SOURCE_PACKAGE_FILE_TYPE_NATIVE = 4
SOURCE_PACKAGE_FILE_TYPE_DIFF_TARBALL = 5

SOURCE_PACKAGE_FILE_TYPE_CHOICES = ((SOURCE_PACKAGE_FILE_TYPE_DSC, 'Source description (.dsc) file'),
                                    (SOURCE_PACKAGE_FILE_TYPE_ORIG_TARBALL, 'Original tarball'),
                                    (SOURCE_PACKAGE_FILE_TYPE_DIFF, 'diff (patch) file'),
                                    (SOURCE_PACKAGE_FILE_TYPE_NATIVE, 'Native tarball'),
                                    (SOURCE_PACKAGE_FILE_TYPE_DIFF_TARBALL, 'Diff tarball (for quilt format)'))


class SourcePackageVersionFile(models.Model):
    source_package_version = models.ForeignKey(SourcePackageVersion)
    filename = models.CharField(max_length=200)
    file_type = models.SmallIntegerField(choices=SOURCE_PACKAGE_FILE_TYPE_CHOICES, null=False)
    size = models.IntegerField()
    md5sum = models.CharField(max_length=32)
    sha1sum = models.CharField(max_length=40)
    sha256sum = models.CharField(max_length=64)

    def __str__(self):
        return '%s' % (self.filename,)

    class Meta:
        unique_together = ('source_package_version', 'file_type')
