# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 22:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def add_architectures(apps, schema_editor):
    Architecture = apps.get_model("buildsvc", "Architecture")
    Architecture.objects.create(name='i386')
    Architecture.objects.create(name='amd64')
    Architecture.objects.create(name='all')


def remove_architectures(apps, schema_editor):
    Architecture = apps.get_model("buildsvc", "Architecture")
    Architecture.objects.filter(name='i386').delete()
    Architecture.objects.filter(name='amd64').delete()
    Architecture.objects.filter(name='all').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('buildsvc', '0024_repository-driver-feature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Architecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BinaryBuild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('architecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.Architecture')),
            ],
        ),
        migrations.CreateModel(
            name='BinaryPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.Repository')),
            ],
        ),
        migrations.CreateModel(
            name='BinaryPackageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=200)),
                ('short_description', models.CharField(default=b'', max_length=255)),
                ('long_description', models.TextField(default=b'')),
                ('package_type', models.SmallIntegerField(choices=[(1, b'Debian package (.deb)'), (2, b'Debian-installer package (.udeb)'), (3, b'Debug Debian package (.ddeb)')], default=1)),
                ('architecture', models.CharField(max_length=32)),
                ('section', models.TextField(null=True)),
                ('priority', models.TextField(null=True)),
                ('maintainer', models.TextField(null=True)),
                ('depends', models.TextField(null=True)),
                ('recommends', models.TextField(null=True)),
                ('suggests', models.TextField(null=True)),
                ('conflicts', models.TextField(null=True)),
                ('replaces', models.TextField(null=True)),
                ('provides', models.TextField(null=True)),
                ('pre_depends', models.TextField(null=True)),
                ('enhances', models.TextField(null=True)),
                ('breaks', models.TextField(null=True)),
                ('installed_size', models.IntegerField(null=True)),
                ('size', models.IntegerField()),
                ('md5sum', models.CharField(max_length=32)),
                ('sha1', models.CharField(max_length=40)),
                ('sha256', models.CharField(max_length=64)),
                ('homepage', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=250)),
                ('binary_build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.BinaryBuild')),
                ('binary_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.BinaryPackage')),
            ],
        ),
        migrations.CreateModel(
            name='SourcePackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.Repository')),
            ],
        ),
        migrations.CreateModel(
            name='SourcePackageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binary', models.TextField()),
                ('architecture', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=50)),
                ('maintainer', models.CharField(max_length=200)),
                ('standards_version', models.CharField(max_length=50)),
                ('build_depends', models.TextField()),
                ('build_depends_indep', models.TextField()),
                ('build_conflicts', models.TextField()),
                ('build_conflicts_indep', models.TextField()),
                ('homepage', models.CharField(max_length=250)),
                ('format', models.CharField(max_length=50)),
                ('package_source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buildsvc.PackageSource')),
                ('source_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.SourcePackage')),
            ],
        ),
        migrations.CreateModel(
            name='SourcePackageVersionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
                ('file_type', models.SmallIntegerField(choices=[(1, b'Source description (.dsc) file'), (2, b'Original tarball'), (3, b'diff (patch) file'), (4, b'Native tarball'), (5, b'Diff tarball (for quilt format)')])),
                ('size', models.IntegerField()),
                ('md5sum', models.CharField(max_length=32)),
                ('sha1sum', models.CharField(max_length=40)),
                ('sha256sum', models.CharField(max_length=64)),
                ('source_package_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.SourcePackageVersion')),
            ],
        ),
        migrations.AddField(
            model_name='binarybuild',
            name='source_package_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildsvc.SourcePackageVersion'),
        ),
        migrations.AddField(
            model_name='series',
            name='source_packages',
            field=models.ManyToManyField(to='buildsvc.SourcePackageVersion'),
        ),
        migrations.AlterUniqueTogether(
            name='sourcepackageversionfile',
            unique_together=set([('source_package_version', 'file_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='sourcepackageversion',
            unique_together=set([('source_package', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='sourcepackage',
            unique_together=set([('name', 'repository')]),
        ),
        migrations.AlterUniqueTogether(
            name='binarypackage',
            unique_together=set([('name', 'repository')]),
        ),
        migrations.RunPython(add_architectures, remove_architectures),
    ]
