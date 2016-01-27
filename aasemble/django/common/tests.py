from django.contrib.auth.models import User

from aasemble.django.common import models
from aasemble.django.common.utils import user_has_feature
from aasemble.django.tests import AasembleTestCase as TestCase


class AasembleUserTestCase(TestCase):
    def test_has_feature_that_is_on_by_default(self):
        user = User.objects.get(id=1)
        self.assertTrue(user_has_feature(user, 'DUMMY_FEATURE'))

    def test_does_not_have_feature_that_is_off_by_default(self):
        user = User.objects.get(id=1)
        self.assertFalse(user_has_feature(user, 'DUMMY_FEATURE_2'))

    def test_user_has_feature_when_given(self):
        user = User.objects.get(id=1)
        feature = models.Feature.objects.get(name='DUMMY_FEATURE_2')
        feature.users.add(user)
        self.assertTrue(user_has_feature(user, 'DUMMY_FEATURE_2'))
