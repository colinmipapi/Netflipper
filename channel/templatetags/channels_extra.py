from django import template

register = template.Library()


@register.filter(name='sec_to_min')
def sec_to_min(runtime):

    min_time = round(runtime/60)

    return min_time
