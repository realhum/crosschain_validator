from django.contrib.admin import ModelAdmin, register

from .models import Contract


# Register your models here.
@register(Contract)
class ContractModelAdmin(ModelAdmin):
    fields = (
        'title',
        'type',
        'address',
        # 'provider',
        'network',
        'abi',
        'blockchain_number',
        'hash_of_creation',
        'percent_of_encreasing_gas_price',
        'min_gas_price',
        'default_average_volume_gas_used',
        'current_gas_price',
        'router_contract',
        '_is_displayed',
    )
    list_display = (
        'id',
        'title',
        'type',
        'address',
        'network',
        'blockchain_number',
        'percent_of_encreasing_gas_price',
        'min_gas_price',
        'current_gas_price',
        'router_contract',
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
        'router_contract',
    )
