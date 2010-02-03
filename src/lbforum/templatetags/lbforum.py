from django import template
from django.utils.html import escape

from postmarkup import create

register = template.Library()

_postmarkup = create(use_pygments=False, annotate_links=False)

@register.filter
def bbcode(s):
    s = escape(s)
    return _postmarkup(s)


@register.filter
def topic_icon(topic): 
    if topic.closed:
        return 'closed'
    elif topic.sticky:
        return 'sticky'
    else:
        return 'normal'

@register.filter
def post_style(forloop):
    styles = ''
    if forloop['first']:
        styles = 'firstpost topicpost'
    else:
        styles = 'replypost'
    if forloop['last']:
        styles += ' lastpost'
    return styles

@register.filter
def online(user):#TODO... to a common app
    return 'Online'
    if user.lbforum_profile.is_online:
        return 'Online'
    return 'Offline'

@register.simple_tag
def page_item_idx(page_obj, forloop):
    return page_obj.start_index() + forloop['counter0']

@register.simple_tag
def page_range_info(page_obj):
    paginator = page_obj.paginator
    if paginator.num_pages == 1:
        return paginator.count
    return str(page_obj.start_index()) +' ' + 'to' + ' ' +  \
            str(page_obj.end_index()) + ' ' + 'of' + ' ' +  str(page_obj.paginator.count)