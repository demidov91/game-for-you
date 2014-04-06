from core.defines import LANGUAGE_DISPLAY_CODE_MAPPING, LANGUAGE_CSS_MAPPING

from django import template

register = template.Library()

def into_css(value):
    """
    Converts lang code into base css class.
    """
    return LANGUAGE_CSS_MAPPING[value]

def into_display_code(value):
    """
    Converts language code into displayable string.
    """
    return LANGUAGE_DISPLAY_CODE_MAPPING[value]

register.filter('into_css', into_css)
register.filter('into_display_code', into_display_code)