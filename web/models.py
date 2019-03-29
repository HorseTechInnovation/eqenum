from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.mail import  EmailMessage,  mail_admins

from countries_plus.models import Country
from languages_plus.models import Language, CultureCode
from languages_plus.utils import associate_countries_and_languages

from markupfield.fields import MarkupField

#from treebeard.mp_tree import MP_Node
#NOTE: can't use treebeard and have ref as primary key

class CreatedUpdatedMixin(models.Model):

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_creator", editable=False,blank=True, null=True, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False, db_index=True)
    updator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_updator", editable=False,blank=True, null=True, on_delete=models.DO_NOTHING,)
    updated = models.DateTimeField(_('Updated Date'), blank=True, null=True, editable=False, db_index=True)

    class Meta:
        abstract = True

class CustomUser(AbstractUser):

    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, blank=True, null=True, on_delete=models.CASCADE)


class UserContact(models.Model):

    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    contact_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=40)
    notes = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)    # use for json data, convert to field when avaialble

    def __str__(self):
        return "%s" % self.user

    def __str__(self):
        return "%s" % self.user

    @classmethod
    def add(cls, user, method, notes=None, data=None):

        obj = cls.objects.create(user=user, method=method, notes=notes, data=data)

        mail_admins("User Contact %s - %s " % (obj.user, obj.method), obj.notes, fail_silently=True)


class Authority(models.Model):
    ref = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    url = models.URLField(blank=True, null=True)
    notes = MarkupField(markup_type='markdown', blank=True, null=True)


class EnumType(CreatedUpdatedMixin):

    ENUMTYPE_STATUS_DEPRECATED = 0
    ENUMTYPE_STATUS_PROPOSED = 1
    ENUMTYPE_STATUS_DRAFT = 3
    ENUMTYPE_STATUS_APPROVED = 6



    ENUMTYPE_STATUS = (
        (ENUMTYPE_STATUS_DEPRECATED, "Deprecated"),
        (ENUMTYPE_STATUS_PROPOSED, "Proposed"),
        (ENUMTYPE_STATUS_DRAFT, "Draft"),
        (ENUMTYPE_STATUS_APPROVED, "Approved"),

    )
    #NOTE: you cannot have ref as the primary key without breaking treebeard
    ref = models.CharField(max_length=20, primary_key=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, unique=True)
    status = models.PositiveSmallIntegerField(default=1, choices=ENUMTYPE_STATUS)
    notes = MarkupField(markup_type='markdown', blank=True, null=True)

    node_order_by = ['name']

    def __str__(self):
        return self.ref

    class Meta:
        verbose_name = _("Enum Grouping")

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

class Enum(CreatedUpdatedMixin):

    ENUM_STATUS_DEPRECATED = 0
    ENUM_STATUS_PROPOSED = 1
    ENUM_STATUS_DRAFT = 3
    ENUM_STATUS_APPROVED = 6

    ENUM_STATUS = (
        (ENUM_STATUS_DEPRECATED, "Incomplete"),
        (ENUM_STATUS_PROPOSED, "Proposed"),
        (ENUM_STATUS_DRAFT,  "Draft"),
        (ENUM_STATUS_APPROVED, "Approved"),

    )
    enumtype = models.ForeignKey(EnumType,on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    ref = models.CharField(max_length=20)
    name = models.CharField(max_length=60)
    status = models.PositiveSmallIntegerField(default=1, choices=ENUM_STATUS)
    ordering = models.CharField(max_length=10, default="0")
    notes = MarkupField(markup_type='markdown', blank=True, null=True)


    def __str__(self):
        return self.ref


    class Meta:
        unique_together = ('enumtype', 'authority', 'ref')
        verbose_name = _("Enum Item")
        ordering = ['ordering','ref']

    @classmethod
    def can_add(self, user):
        return user.is_superuser

    def can_edit(self, user):
        return user.is_superuser or user == self.creator

    def can_delete(self, user):
        return (user.is_superuser or user == self.creator) and self.is_deletable

    @property
    def is_deleteable(self):
        #TODO: return false if this enum is used by any of the models
        return True

class EnumDisplay(CreatedUpdatedMixin):
    '''
    "language": "en",
        "culture": "en-US",
        "display": "SKEnumTypes",
        "abbreviation": "",
        "symbol": "" }]
    '''

    enum = models.ForeignKey(Enum,  on_delete=models.CASCADE)
    # language MUST be provided and can be derived from culture
    language = models.ForeignKey(Language,  on_delete=models.CASCADE)
    # culture is optional - or should it be required with a default per language
    culture = models.ForeignKey(CultureCode, blank=True, null=True,  on_delete=models.CASCADE)
    display = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    symbol = models.CharField(max_length=10, blank=True, null=True)
    notes = MarkupField(markup_type='markdown', blank=True, null=True)

    def __str__(self):
        return self.display

    class Meta:
        verbose_name = _("Enum Output/Display")

    def save(self, *args, **kwargs):

        # language can be derived from culture
        if self.culture and not self.language:
            self.language = self.culture[0:1]


        super().save(*args, **kwargs)