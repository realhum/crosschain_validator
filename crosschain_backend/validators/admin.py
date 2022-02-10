from django.contrib.admin import ModelAdmin, register
from rangefilter.filters import DateTimeRangeFilter

from .models import Validator, ValidatorSwap


@register(Validator)
class ValidatorAdmin(ModelAdmin):
    fields = (
        'title',
        'type',
        '_is_displayed',
    )
    list_display = (
        'id',
        'title',
        'type',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    list_filter = (
        ('_created_at', DateTimeRangeFilter),
        ('_updated_at', DateTimeRangeFilter),
        '_is_displayed',
    )
    search_fields = (
        '=id',
        'title',
        'trade__from_onchain_swap__transaction__hash',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'


@register(ValidatorSwap)
class ValidatorSwapAdmin(ModelAdmin):
    fields = (
        'contract',
        'transaction',
        'signature',
        'status',
        '_is_displayed',
    )
    list_display = (
        'id',
        'contract',
        'transaction',
        'signature',
        'status',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    list_filter = (
        'contract',
        'status',
        'contract__network__title',
        ('_created_at', DateTimeRangeFilter),
        ('_updated_at', DateTimeRangeFilter),
        '_is_displayed',
    )
    search_fields = (
        '=id',
        'transaction__hash',
        'signature',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'
    autocomplete_fields = (
        'contract',
        'transaction',
    )
