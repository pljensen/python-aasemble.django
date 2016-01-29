from unittest import TestCase

from .binary_package_version import split_description


class BinaryPackageVersionTestCase(TestCase):
    def test_split_description_empty(self):
        self.assertEquals(split_description(''), ('', ''))

    def test_split_description_no_long_description(self):
        self.assertEquals(split_description('Only a short description'),
                          ('Only a short description', ''))

    def test_split_description_full(self):
        self.assertEquals(split_description('a short description\n ...and a long\n .\n description, too\n'),
                          ('a short description', '...and a long\n.\ndescription, too\n'))
