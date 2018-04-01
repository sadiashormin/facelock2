from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from home.forms import HomeForm
from home.models import Post, Friend
import face_recognition
import os


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        form = HomeForm()
        # posts = Post.objects.all().order_by('-created')
        posts = Post.objects.filter(user_id__in=Friend.objects.get(
            current_user=request.user).users.all()) | Post.objects.filter(user=request.user)
        posts = posts.order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
        except:
            friend = None
            friends = None

        args = {
            'form': form, 'posts': posts, 'users': users, 'friends': friends
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

            friendsPicFileName = ['mahbub.jpg', 'sadia.jpg', 'shaila.jpg']
            uploadedPhotoName = "sadiamahbub.jpg"
            uploadedPhoto = face_recognition.load_image_file(os.path.abspath(os.path.dirname(__file__))+"/static/"+uploadedPhotoName)
            uploadedPhotoEncodlings = face_recognition.face_encodings(uploadedPhoto)
            for unknownFaceEncoding in uploadedPhotoEncodlings:
                for friendPicFileName in friendsPicFileName:
                    fndpic = face_recognition.load_image_file(os.path.abspath(os.path.dirname(__file__))+"/static/"+friendPicFileName)
                    friendpicEncoding = face_recognition.face_encodings(fndpic)[0]
                    results = face_recognition.compare_faces([unknownFaceEncoding], friendpicEncoding)

                    if results[0] == True:
                        b=2
                    else:
                        c=3

            # picture_of_me = face_recognition.load_image_file(
            #     os.path.abspath(os.path.dirname(__file__))+"/static/sadia.jpg")
            # # face_locations = face_recognition.face_locations(picture_of_me)

            # # picture_of_me = face_recognition.load_image_file("me.jpg")
            # my_face_encoding = face_recognition.face_encodings(picture_of_me)[
            #     0]

            # # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

            # unknown_picture = face_recognition.load_image_file(
            #     os.path.abspath(os.path.dirname(__file__))+"/static/sadiamahbub.jpg")
            # unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[
            #     1]

            # # Now we can see the two face encodings are of the same person with `compare_faces`!

            # results = face_recognition.compare_faces(
            #     [my_face_encoding], unknown_face_encoding)

            # if results[0] == True:
            #     print("It's a picture of me!")
            # else:
            #     print("It's not a picture of me!")

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
