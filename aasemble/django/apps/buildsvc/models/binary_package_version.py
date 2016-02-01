import hashlib
import os.path

import deb822

from django.conf import settings
from django.core.files.base import File
from django.db import models

from aasemble.django.apps.buildsvc import storage
from aasemble.django.apps.buildsvc.models.architecture import Architecture
from aasemble.django.apps.buildsvc.models.binary_build import BinaryBuild
from aasemble.django.apps.buildsvc.models.binary_package import BINARY_PACKAGE_TYPE_CHOICES, BINARY_PACKAGE_TYPE_DEB, BinaryPackage
from aasemble.django.apps.buildsvc.models.source_package import SourcePackage
from aasemble.django.apps.buildsvc.models.source_package_version import SourcePackageVersion


def split_description(description):
    if description == '':
        return '', ''

    if '\n' not in description:
        return description, ''

    lines = description.split('\n')
    return lines[0], '\n'.join([l[1:] for l in lines[1:]])


def join_description(short_description, long_description):
    return short_description + (long_description and (''.join(['\n %s' % l for l in long_description.split('\n')])) or '').rstrip(' ')


class BinaryPackageVersion(models.Model):
    binary_package = models.ForeignKey(BinaryPackage)
    version = models.CharField(max_length=200, null=False)
    short_description = models.CharField(max_length=255, null=False, default='')
    long_description = models.TextField(null=False, default="")
    binary_build = models.ForeignKey(BinaryBuild)
    package_type = models.SmallIntegerField(choices=BINARY_PACKAGE_TYPE_CHOICES, default=BINARY_PACKAGE_TYPE_DEB)
    architecture = models.CharField(max_length=32)
    section = models.TextField(null=True)
    priority = models.TextField(null=True)
    maintainer = models.TextField(null=True)
    depends = models.TextField(null=True)
    recommends = models.TextField(null=True)
    suggests = models.TextField(null=True)
    conflicts = models.TextField(null=True)
    replaces = models.TextField(null=True)
    provides = models.TextField(null=True)
    pre_depends = models.TextField(null=True)
    enhances = models.TextField(null=True)
    breaks = models.TextField(null=True)
    installed_size = models.IntegerField(null=True)
    size = models.IntegerField()
    md5sum = models.CharField(max_length=32)
    sha1 = models.CharField(max_length=40)
    sha256 = models.CharField(max_length=64)
    homepage = models.CharField(max_length=250)
    location = models.CharField(max_length=250)

    known_fields = ('Version',
                    'Architecture',
                    'Maintainer',
                    'Installed-Size',
                    'Depends',
                    'Recommends',
                    'Suggests',
                    'Conflicts',
                    'Replaces',
                    'Provides',
                    'Pre-Depends',
                    'Enhances',
                    'Breaks',
                    'Priority',
                    'Section',
                    'Homepage')

    fileinfo_fields = ('Size',
                       'Filename',
                       'MD5Sum',
                       'SHA1Sum',
                       'SHA256Sum')

    def __str__(self):
        return '%s_%s_%s' % (self.binary_package.name, self.version, self.binary_build.architecture)

    @property
    def filename(self):
        sp = self.binary_build.source_package_version.source_package
        return 'pool/main/%s/%s/%s_%s_%s.deb' % (sp.name[0], sp.name, self.binary_package.name, self.version, self.architecture)

    def format_for_packages(self):
        data = deb822.Deb822()
        data['Package'] = self.binary_package.name

        data['Source'] = self.binary_build.source_package_version.source_package.name

        for field in self.known_fields:
            value = getattr(self, field.lower().replace('-', '_'))
            if value:
                data[field] = str(value)

        data['Filename'] = self.filename

        for field in self.fileinfo_fields:
            data[field] = str(getattr(self, field.lower().replace('-', '_')))

        data['Description'] = join_description(self.short_description, self.long_description)
        return str(data)

    def store(self, fpath):
        destpath = os.path.join(self.binary_build.source_package_version.source_package.repository.user.username,
                                self.binary_build.source_package_version.source_package.repository.name,
                                self.filename)
        storage_driver = storage.get_repository_storage_driver()
        with open(fpath, 'rb') as fp:
            storage_driver.save(destpath, File(fp))

    @classmethod
    def import_file(cls, repository, path):
        from aasemble.django.utils import run_cmd
        out = run_cmd(['dpkg-deb', '-I', path, 'control'])

        control = deb822.Deb822(out)

        bb_info = {'source_package': None,
                   'version': None,
                   'architecture': None}

        known_fields_lowercase = [f.lower() for f in cls.known_fields]

        kwargs = {}
        for k in control:
            k_lower = k.lower()
            if k_lower == 'package':
                bp, _ = BinaryPackage.objects.get_or_create(name=control[k], repository=repository)
                kwargs['binary_package'] = bp
            elif k_lower == 'source':
                bb_info['source_package'], _ = SourcePackage.objects.get_or_create(name=control[k], repository=repository)
            elif k_lower == 'version':
                kwargs['version'] = control[k]
                bb_info['version'] = control[k]
            elif k_lower == 'architecture':
                bb_info['architecture'] = Architecture.objects.get(name=control[k])
                kwargs['architecture'] = control[k]
            elif k_lower in known_fields_lowercase:
                kwargs[k.lower().replace('-', '_')] = control[k]
            elif k_lower == 'description':
                kwargs['short_description'], kwargs['long_description'] = split_description(control[k])

        if not bb_info['source_package']:
            bb_info['source_package'], _ = SourcePackage.objects.get_or_create(name=path.split('/')[-2], repository=repository)

        if all(bb_info.values()):
            spv, _ = SourcePackageVersion.objects.get_or_create(source_package=bb_info['source_package'], version=bb_info['version'])
            spv.series_set.add(repository.first_series())
            kwargs['binary_build'], _ = BinaryBuild.objects.get_or_create(source_package_version=spv, architecture=bb_info['architecture'])

        with open(path, 'rb') as fp:
            contents = fp.read()

        kwargs['md5sum'] = hashlib.md5(contents).hexdigest()
        kwargs['sha1'] = hashlib.sha1(contents).hexdigest()
        kwargs['sha256'] = hashlib.sha256(contents).hexdigest()
        kwargs['size'] = len(contents)

        self, _ = cls.objects.get_or_create(**kwargs)
        self.store(path)
