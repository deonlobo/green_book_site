from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Question, Tag

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].required = False

    def clean_tags(self):
        tag_names = self.cleaned_data['tags'].split(',')
        return [tag_name.strip() for tag_name in tag_names if tag_name.strip()]

    class Meta:
        model = Question
        fields = ('title', 'body')
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='body_config'
            )
        }
