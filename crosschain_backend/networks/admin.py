from django.contrib.admin import register, ModelAdmin

from .models import Network, Transaction


# Register your models here.
@register(Network)
class NetworkModelAdmin(ModelAdmin):
    fields = (
        'title',
        'rpc_url_list',
        '_is_displayed',
    )
    list_display = (
        'id',
        'title',
        'rpc_url_list',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    list_filter = (
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    search_fields = (
        '=id',
        'title',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'


@register(Transaction)
class TransactionModelAdmin(ModelAdmin):
    fields = (
        'network',
        'hash',
        'block_hash',
        'block_number',
        'sender',
        'receiver',
        'gas',
        'gas_price',
        'nonce',
        'sign_r',
        'sign_s',
        'sign_v',
        'index',
        'type',
        'value',
        'data',
        'event_data',
        '_is_displayed',
    )
    list_display = (
        'id',
        'network',
        'hash',
        'block_number',
        'sender',
        'receiver',
        'gas',
        'gas_price',
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
        'hash',
        'sender',
        'receiver',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'
    autocomplete_fields = (
        'network',
    )
