from django import template
from elements.models import Element

register = template.Library()

@register.filter
def get_element_by_id(product_id):
    try:
        return Element.objects.get(id=product_id)
    except Element.DoesNotExist:
        return None