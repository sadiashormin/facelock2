from django import template
from home.models import Post, Friend, Tag
from accounts.models import Face

register = template.Library()

@register.filter
def getTags(post):
    # return post.id
    return Tag.objects.filter(post_id=post.id).all()

@register.filter
def getFace(user):
    # return post.id
    try:
        face =Face.objects.get(user=user)
    except:
        face=None
    return face

@register.filter
def shouldVisible(post, loggedInUser):
    tags = Tag.objects.filter(post_id=post.id).all()
    visible = True
    if post.user.id != loggedInUser.id:
        amiItagged = False
        for tag in tags:
            if tag.user_id == loggedInUser.id:
                amiItagged = True
            if tag.status == 0 or tag.status == 2:
                visible = False
        if amiItagged == True:
            visible = True
    return visible

@register.filter
def postItAnyWayEnabled(post, loggedInUser):
    tags = Tag.objects.filter(post_id=post.id).all()
    postItAnyWayEnabled = False
    if post.user.id == loggedInUser.id:
        isPending = False
        hasAnyOneRejected= False
        for tag in tags:
            if tag.user_id != loggedInUser.id:
                if tag.status == 0:
                    isPending = True
                if tag.status == 2:
                    hasAnyOneRejected = True
        if isPending == False and hasAnyOneRejected == True:
            postItAnyWayEnabled = True
    return postItAnyWayEnabled