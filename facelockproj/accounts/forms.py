from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        
class EditProfileForm(forms.ModelForm):
    template_name='/something/else'

    class Meta:
        model = UserProfile
        # exclude=('User',)
        fields = (
            # 'first_name',
            # 'last_name',
            'image',
            # 'city'
        )
    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=False)
        # profile.city = self.cleaned_data['city']
        #profile.image=self.cleaned_data['image']

        if commit:
            profile.save()

        return profile
