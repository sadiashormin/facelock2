from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.models import Face
from home.forms import HomeForm
from home.models import Post, Friend, Tag
import face_recognition
import cv2
import os
from django import template

# Imports the Google Cloud client library---->
import io
import os
from google.cloud import vision
from google.cloud.vision import types
# <----
import time
from latlon import get_exif_data, get_lat_lon,get_timespan

register = template.Library()

# @register.simple_tag
# def getTags():
#     return Tag.count
# @register.filter
# def lower(value):
#     return value.lower()

class HomeView(TemplateView):
    template_name = 'home/home.html'
   
   
    def get(self, request):
        
        form = HomeForm()
        # posts = Post.objects.all().order_by('-created')
        posts = None
       #request.GET.get('Search')
        users = User.objects.exclude(id=request.user.id)
        if request.GET.get('Search') != None:
             users =User.objects.filter(username__startswith=request.GET.get('Search')).exclude(id=request.user.id)
        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            posts = Post.objects.filter( user_id__in=Friend.objects.get(current_user=request.user).users.all()) | Post.objects.filter(user=request.user)
            posts = posts.order_by('-created')
        except:
            friend = None
            friends = None
            posts =  Post.objects.filter(user=request.user)
            posts = posts.order_by('-created')

        args = {
            'form': form, 'posts': posts, 'users': users[:5], 'friends': friends,"loggedInUser": request.user
        }
        return render(request, self.template_name, args)
    
    def post(self, request):
        form = HomeForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.status = 1
            post.save()
            
            text = form.cleaned_data['post']
            form = HomeForm()

            # friend = None
            # friends = None
           

            tagLabelMetaSave(post, request)
            return redirect('home:home')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)


def tagLabelMetaSave(post, request):
    if(post.picture):
        post.status = 0
        friendfaces=None;
        try:
            friend = Friend.objects.get(current_user=request.user)
            friendfaces=Face.objects.filter(user_id__in=friend.users.all())
        except:
            pass
        uploadedPhoto = face_recognition.load_image_file(os.path.abspath(os.path.dirname(__file__))+"/static/"+post.picture.name)
        uploadedPhotoEncodlings = face_recognition.face_encodings(uploadedPhoto)
        # taggedPersonsNameString="";
        for i in range(0,len(uploadedPhotoEncodlings)):
            for friendface in friendfaces:
                fndpic = face_recognition.load_image_file(os.path.abspath(os.path.dirname(__file__))+"/static/"+friendface.picture.name)
                friendpicEncoding = face_recognition.face_encodings(fndpic)[0]
                results = face_recognition.compare_faces([uploadedPhotoEncodlings[i]], friendpicEncoding, tolerance=0.48)
                if results[0] == True:
                    # taggedPersonsNameString=taggedPersonsNameString+friendface.user.username+","
                    face_locations = face_recognition.face_locations(uploadedPhoto)
                    top, right, bottom, left = face_locations[i]

                    t = Tag()
                    t.user=friendface.user
                    t.post=post
                    t.status=0
                    t.top=int(top)
                    t.right=int(right)
                    t.bottom=int(bottom)
                    t.left=int(left)
                    t.save()
                    
                else:
                    c=3
        labels=googlecloudplatformexperiement(post.picture.name)
        lat,lon = get_lat_lon(get_exif_data(os.path.abspath(os.path.dirname(__file__))+"/static/"+post.picture.name))
        if post.lat == None:
            post.lat=lat
            post.lon=lon
            post.timestamp=get_timespan(get_exif_data(os.path.abspath(os.path.dirname(__file__))+"/static/"+post.picture.name))
        post.labels=labels
        
        post.save()

def googlecloudplatformexperiement(imagename):
    client = vision.ImageAnnotatorClient()
    file_name=os.path.abspath(os.path.dirname(__file__))+"/static/"+imagename
    # file_name = os.path.join(
    #     os.path.dirname(__file__),
    #     "/static/"+imagename)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    labelcsv=""
    for label in labels:
        if labelcsv =="":
            labelcsv= label.description
        else:
            labelcsv= labelcsv+","+label.description
    return labelcsv

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:home')

def action_tag(request, operation, pk, area=None):

    if operation == 'approve':
        tag = Tag.objects.get(pk=pk)
        tag.status=1
        tag.save()
    elif operation == 'reject':
        tag = Tag.objects.get(pk=pk)
        tag.status=2
        tag.save()
        post = tag.post
        picToBlur=post.bluredPicture.name if post.bluredPicture else tag.post.picture.name
        #uploadedPhoto = face_recognition.load_image_file(os.path.abspath(os.path.dirname(__file__))+"/static/"+tag.post.picture.name)
        frame = cv2.imread(os.path.abspath(os.path.dirname(__file__))+"/static/"+picToBlur)
        # 240/500
        height, width, channels = frame.shape 
        if area == None:
            face_image = frame[tag.top:tag.bottom, tag.left:tag.right]  
            face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
            frame[tag.top:tag.bottom, tag.left:tag.right] = face_image
            cv2.imwrite(os.path.abspath(os.path.dirname(__file__))+"/static/"+"blured"+picToBlur,frame)
        else:
            tag.status=3
            tag.save()
            # area = '10:20:60:100 20110:119:183:266 20348:57:123:212 20355:334:76:124'
            viewWidth=int(area.split("!")[0])
            ratio=float(width)/viewWidth
            sections=area.split("!")[1].split(" ")
            for section in sections:
                points=map(int,section.split(":"))
                face_image = frame[int(points[1]*ratio) :int((points[1]+points[3])*ratio), int(points[0]*ratio):int((points[0]+points[2])*ratio)]  
                face_image = cv2.GaussianBlur(face_image, (99, 99), 90)
                frame[int(points[1]*ratio) :int((points[1]+points[3])*ratio), int(points[0]*ratio):int((points[0]+points[2])*ratio)] = face_image
                cv2.imwrite(os.path.abspath(os.path.dirname(__file__))+"/static/"+"blured"+picToBlur,frame)

        post.bluredPicture="blured"+picToBlur
        post.save()
        # find the post and the image path
        # use lib to recognize current user
    if operation == 'checkpost':
        post = Post.objects.get(pk=pk)

        picToBlur=post.bluredPicture.name if post.bluredPicture else post.picture.name
        frame = cv2.imread(os.path.abspath(os.path.dirname(__file__))+"/static/"+picToBlur)
        height, width, channels = frame.shape 
        viewWidth=int(area.split("!")[0])
        ratio=float(width)/viewWidth
        sections=area.split("!")[1].split(" ")
        for section in sections:
            points=map(int,section.split(":"))
            face_image = frame[int(points[1]*ratio) :int((points[1]+points[3])*ratio), int(points[0]*ratio):int((points[0]+points[2])*ratio)]  
            face_image = cv2.GaussianBlur(face_image, (99, 99), 90)
            frame[int(points[1]*ratio) :int((points[1]+points[3])*ratio), int(points[0]*ratio):int((points[0]+points[2])*ratio)] = face_image
            cv2.imwrite(os.path.abspath(os.path.dirname(__file__))+"/static/"+"blured"+picToBlur,frame)
        post.bluredPicture="blured"+picToBlur
        # post.save()

        post.label = None
        Tag.objects.filter(post_id=post.id).filter(status=1).delete()
        Tag.objects.filter(post_id=post.id).filter(status=2).delete()
        Tag.objects.filter(post_id=post.id).filter(status=3).delete()
        post.picture=post.bluredPicture
        post.bluredPicture= None;
        post.save()
        tagLabelMetaSave(post,request)

    return redirect('home:home')



def action_post(request, operation, pk):
    post = Post.objects.get(pk=pk)
    if operation == 'delete':
        post.delete()
    if operation == 'postItAnyway':
        Tag.objects.filter(post_id=post.id).filter(status=2).delete()
        Tag.objects.filter(post_id=post.id).filter(status=3).delete()
        post.picture=post.bluredPicture
        post.bluredPicture= None;
        post.save()
    if operation == 'confirmed':
        post.status=1
        post.save()
    
    # post.tags
    # post.delete()
# elif operation == 'reject':
#     tag.status=2
#     tag.save()
    return redirect('home:home')

