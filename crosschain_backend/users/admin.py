from django.contrib.admin import register, site
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
    GroupAdmin as BaseGroupAdmin,
)
from django.utils.translation import gettext_lazy as _

from .models import (
    BaseGroup,
    Group,
    User,
)


# Register your models here.
site.unregister(BaseGroup)


@register(User)
class UserModelAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email',)
            }
        ),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_superuser',
        'last_login',
        '_created_at',
        '_updated_at',
        '_is_displayed',

    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'last_login',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    ordering = (
        '-is_staff',
        '-is_superuser',
        '-last_login',
    )
    empty_value_display = '-empty-'


@register(Group)
class GroupModelAdmin(BaseGroupAdmin):
    list_display = (
        'id',
        'name',
        '_created_at',
        '_updated_at',
        '_is_displayed',

    )
    list_filter = (
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    ordering = (
        '-_created_at',
    )

    empty_value_display = '-empty-'
