from django.contrib.admin import ModelAdmin, register

from .models import Contract


# Register your models here.
@register(Contract)
class ContractModelAdmin(ModelAdmin):
    fields = (
        'title',
        'type',
        'address',
        'network',
        'abi',
        'blockchain_number',
        'hash_of_creation',
        '_is_displayed',
    )
    list_display = (
        'id',
        'title',
        'type',
        'address',
        'network',
        'blockchain_number',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    list_filter = (
        'type',
        'network__title',
        'blockchain_number',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    search_fields = (
        '=id',
        'title',
        'address',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'
    autocomplete_fields = (
        'network',
    )
