
from django.test import TestCase, override_settings
from django.core.exceptions import ImproperlyConfigured, ValidationError

from django.db import IntegrityError
from django.utils import timezone


from nose.tools import assert_equal, with_setup, assert_false, eq_, ok_
from unittest import skip

from web.models import *

from django.contrib.auth import get_user_model
User = get_user_model()


@override_settings(TESTING = True)
class EnumTest(TestCase):
    ''' add basic data
    '''

    def test_add_enum_no_enumtype(self):
        pass