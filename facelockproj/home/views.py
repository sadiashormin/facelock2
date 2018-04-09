from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.models import Face
from home.forms import HomeForm
from home.models import Post, Friend, Tag
import face_recognition
import os
from django import template

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
       
        users = User.objects.exclude(id=request.user.id)
        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            posts = Post.objects.filter(user_id__in=Friend.objects.get(current_user=request.user).users.all()) | Post.objects.filter(user=request.user)
            posts = posts.order_by('-created')
        except:
            friend = None
            friends = None
            posts =  Post.objects.filter(user=request.user)
            posts = posts.order_by('-created')

        args = {
            'form': form, 'posts': posts, 'users': users, 'friends': friends,"loggedInUser": request.user
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            text = form.cleaned_data['post']
            form = HomeForm()

            # friend = None
            # friends = None
            friendfaces=None;
            try:
                friend = Friend.objects.get(current_user=request.user)
                # friends = friend.users.all()
                friendfaces=Face.objects.filter(user_id__in=friend.users.all())
            except:
                pass

            if(post.picture):
                uploadedPhoto = face_recognition.load_image_file(os.path.abspath(os.path.dirname(__file__))+"/static/"+post.picture.name)
                uploadedPhotoEncodlings = face_recognition.face_encodings(uploadedPhoto)
                # taggedPersonsNameString="";
                for unknownFaceEncoding in uploadedPhotoEncodlings:
                    for friendface in friendfaces:
                        fndpic = face_recognition.load_image_file(os.path.abspath(os.path.dirname(__file__))+"/static/"+friendface.picture.name)
                        friendpicEncoding = face_recognition.face_encodings(fndpic)[0]
                        results = face_recognition.compare_faces([unknownFaceEncoding], friendpicEncoding, tolerance=0.56)

                        if results[0] == True:
                            # taggedPersonsNameString=taggedPersonsNameString+friendface.user.username+","
                            t = Tag()
                            t.user=friendface.user
                            t.post=post
                            t.approved=False
                            t.save()
                            
                        else:
                            c=3
            # if(taggedPersonsNameString):
            #     post.post=post.post+"<br/>TAGGED " +taggedPersonsNameString
            #     post.save()
            
            return redirect('home:home')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:home')

def action_tag(request, operation, pk):
    tag = Tag.objects.get(pk=pk)
    if operation == 'approve':
        tag.approved=True
        tag.save()
    elif operation == 'reject':
        tag.approved=False
        tag.save()
    return redirect('home:home')
