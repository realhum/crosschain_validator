from uuid import uuid4

from django.db.models import (
    BooleanField,
    DateTimeField,
    Model,
    UUIDField,
)
from django.db.models.manager import Manager

# Create your models here.
class BaseDisplayedManager(Manager):
    """
    Modified Manager for AbstractBaseModel
    """

    def get_queryset(self):
        return super().get_queryset().filter(_is_displayed=True)


class AbstractBaseModel(Model):
    """
    Abstract Base model which inherited by every model in project
    """

    id = UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
    )
    _created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    _updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
    )
    _is_displayed = BooleanField(
        verbose_name='Is displayed',
        default=True,
    )
    # -- Manager
    objects = Manager()
    displayed_objects = BaseDisplayedManager()
    # --

    class Meta:
        abstract = True
