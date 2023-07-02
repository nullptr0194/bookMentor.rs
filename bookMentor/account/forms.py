from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('smer', 'godina')


class AddCourseForm(forms.Form):
    grade = forms.CharField(label='Grade(1-5): ')

    def clean_grade(self):
        cd = self.cleaned_data
        if int(cd['grade']) < 1:
            cd['grade'] = '1'
        elif int(cd['grade']) > 5:
            cd['grade'] = '5'
        else:
            pass
        return cd['grade']
