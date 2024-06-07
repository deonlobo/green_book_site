from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from accounts.models import UserProfile


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    address = forms.CharField(max_length=255, required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Retype Password'})

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.update_or_create(user=user, defaults={'address': self.cleaned_data['address']})
        return user