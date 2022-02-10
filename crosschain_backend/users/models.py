from uuid import uuid4

from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db.models import UUIDField
from django.utils.translation import gettext_lazy as _

from base.models import AbstractBaseModel


# Create your models here.
class User(AbstractUser, AbstractBaseModel):
    id = UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
    )

    class Meta:
        db_table='users'

    def __str__(self) -> str:
        return f'{self.username} (id: {self.id})'

    def save(self, *args, **kwargs):
        self.username = self.username.lower()

        return super().save(*args, **kwargs)


class Group(BaseGroup, AbstractBaseModel):
    def __str__(self) -> str:
        return f'{self.name} (id: {self.id})'
