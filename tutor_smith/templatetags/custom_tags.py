from django.template import Library

register = Library()

# Range Tag for creating range loops in templates
@register.filter(name='range')
def get_range(value):
    """
    Usage:
      <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
      {% endfor %}</ul>
    """
    return range(value)
