from django.contrib.admin import ModelAdmin, register


# Register your models here.
from .models import Token


@register(Token)
class TokenAdmin(ModelAdmin):
    fields = (
        'network',
        'name',
        'symbol',
        'address',
        'decimals',
    )
    list_display = (
        'id',
        'network',
        'name',
        'symbol',
        'address',
        'decimals',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    list_filter = (
        'network__title',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    search_fields = (
        '=id',
        'name',
        'symbol',
        'address',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'
    autocomplete_fields = (
        'network',
    )
