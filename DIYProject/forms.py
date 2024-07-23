from django import forms
from django.forms.models import ModelForm
from DIYProject.models import Project, Thought
class NewProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['posted_by', 'posted_at']

        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'CATEGORY'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
            'image_1': forms.FileInput(attrs={'class': 'form-control', 'style': 'padding-top: 1em; padding-left: 1.5em;'}),
            'image_2': forms.FileInput(attrs={'class': 'form-control', 'style': 'padding-top: 1em; padding-left: 1.5em;'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image_2'].required = False

class ThoughtForm(forms.ModelForm):
    class Meta:
        model = Thought
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control mb-1', 'placeholder': 'Express your thoughts', 'rows':'3','cols':'100%', 'style': 'width: 100%; resize: none;'}),}


class SearchProject(forms.Form):
    term  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-3', 'placeholder': 'Search Projects '}),)