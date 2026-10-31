from django import template

register = template.Library()

@register.filter
def times(number):
    """Loop N times. 4.5 -> 4 stars"""
    try:
        return range(int(float(number)))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def get_item(obj, key):
    """
    Safe dict/list lookup in template: {{ mydict|get_item:key }} or {{ mylist|get_item:0 }}
    Returns None if key/index is missing, empty, or invalid. Never raises.
    """
    if obj is None or key == '':
        return None

    # Dict lookup
    if isinstance(obj, dict):
        return obj.get(key)

    # List/tuple/string index lookup
    try:
        index = int(key)
        return obj[index]
    except (IndexError, ValueError, TypeError, KeyError):
        return None

@register.filter
def mask_account(account):
    """Show last 2 chars only: 123456 -> 3456**"""
    account = str(account or '')
    if len(account) <= 1:
        return 'fail'
    return account[:2] + ''