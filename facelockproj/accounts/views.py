from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
    UserForm,
    FaceForm
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from accounts.models import Face

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login'))
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        # form = EditProfileForm(request.POST, instance=request.user)
        user_form = UserForm(request.POST, instance=request.user)
        if  user_form.is_valid():
            user_form.save()
            # form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        user_form = UserForm(instance=request.user)
        # profile_form = EditProfileForm(instance=request.user)
        # args = {'profile_form': profile_form, 'user_form': user_form}
        args = { 'user_form': user_form}
        return render(request, 'accounts/edit_profile.html', args)

def edit_face(request):
    if request.method == 'POST':
        # form = EditProfileForm(request.POST, instance=request.user)
        face_form = FaceForm(request.POST, request.FILES)
        if  face_form.is_valid():
            if(Face.objects.get(user=request.user)):
                Face.objects.get(user=request.user).delete()

            face = face_form.save(commit=False)
            face.user = request.user
            face.save()
            # face_form.save()
            # form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        face_form = FaceForm(instance=request.user)
        # profile_form = EditProfileForm(instance=request.user)
        # args = {'profile_form': profile_form, 'user_form': user_form}
        args = { 'face_form': face_form}
        return render(request, 'accounts/edit_face.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
