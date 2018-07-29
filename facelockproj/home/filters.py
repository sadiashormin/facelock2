from django import template
from home.models import Post, Friend, Tag
from accounts.models import Face
import decimal
from datetime import datetime, timedelta
from sets import Set
from scipy import spatial
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
    if post.status == 0 and post.user.id != loggedInUser.id:
        return False 
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
                if tag.status == 2 or tag.status == 3:
                    hasAnyOneRejected = True
        if isPending == False and hasAnyOneRejected == True:
            postItAnyWayEnabled = True
    return postItAnyWayEnabled

@register.filter
def showPossibleInferredPost(post, loggedInUser):
    if post.timestamp!=None and post.lat!=None and  post.lon!=None:

        friend = Friend.objects.get(current_user=loggedInUser)
        friends = friend.users.all()
        posts = Post.objects.filter( user_id__in=Friend.objects.get(current_user=loggedInUser).users.all() ).exclude(user_id = loggedInUser.id )
        #remove post without lat long & time
        # posts = posts.exclude(user_id=loggedInUser.id)
        posts = posts.exclude(lat = None);
        posts = posts.exclude(lon = None);
        posts = posts.exclude(timestamp = None);
        radius=decimal.Decimal(.001) #.1 mile radius
        hourDiff= 1 # 1 hour
        

        # remove post which are farther than .2 mile
        posts = posts.exclude( lat__gt=(post.lat+radius));
        posts = posts.exclude( lat__lt=(post.lat-radius));

        posts = posts.exclude( lon__gt=(post.lon+radius));
        posts = posts.exclude( lon__lt=(post.lon-radius));

        # remove post which are not taken within an hour
        minTime=post.timestamp - timedelta(hours=hourDiff)
        posts = posts.exclude( timestamp__lt=minTime);

        maxTime=post.timestamp + timedelta(hours=hourDiff)
        posts = posts.exclude( timestamp__gt=maxTime);
        

        #remove post which are not exposed to friends yet.
        posts = posts.exclude( status=0);
    
        posts = posts.order_by('-created')
        return posts
    return []


@register.filter
def getSimilarity(post, infPost):
    
    pl=post.labels.split(',')
    ipl=infPost.labels.split(',')
    pd={}
    for l in pl:
        pd[l.split(":")[0]]=l.split(":")[1]
    ipd={}
    for l in ipl:
        ipd[l.split(":")[0]]=l.split(":")[1]




    unionLables=list(set.union(set(pd.keys()),set(ipd.keys())))

    f=[]
    fPrime=[]
    for l in unionLables:
        if l in pd:
            f.append(float(pd[l]))
        if l not in  pd:
            f.append(float(0))
        if l in ipd:
            fPrime.append(float( ipd[l]))
        if l not in ipd:
            fPrime.append(float(0))

        
    cosineSimilarity = 1 - spatial.distance.cosine(f, fPrime)
    euclideanDistance = spatial.distance.euclidean(f, fPrime)
    commonLables=list(set.intersection(set(pd.keys()),set(ipd.keys())));
#  return [cosineSimilarity,euclideanDistance, list(set.intersection(set(pd.keys()),set(ipd.keys())))];
    return [cosineSimilarity,euclideanDistance,commonLables];