from django import template
from home.models import Post, Friend, Tag


register = template.Library()

@register.filter
def lower(post):
    # return post.id
    return Tag.objects.filter(post_id=post.id).all()