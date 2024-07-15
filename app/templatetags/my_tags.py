from django import template
from urllib.parse import urlencode, parse_qs

register = template.Library()


@register.simple_tag
def my_url(value, field_name, urlencode=None, **kwargs):
    url = "?{}={}".format(field_name, value)
    
    if urlencode:
        qs = urlencode.split("&")
        filtered_qs = filter(lambda p: p.split("=")[0] != field_name, qs)
        encoded_qs = "&".join(filtered_qs)
        url = "{}&{}".format(url, encoded_qs)
        
    return url


@register.filter
def remove_page_param(query_string):
    query_dict = parse_qs(query_string)
    query_dict.pop('page', None)
    return urlencode(query_dict, doseq=True)
