from django import template


register = template.Library()


@register.simple_tag
def division(divisible, divider, **kwargs):
    """Dividing two numbers"""
    quotient = float(divisible) / float(divider)
    flag = kwargs.get('to_int', False)
    if flag is True:
        return int(quotient)
    elif flag is False:
        return quotient


@register.filter()
def inc(value, number):
    """Summarize some number and value"""
    try:
        value = int(value)
        number = int(number)
        value += number
        return value
    except ValueError as error:
        pass
