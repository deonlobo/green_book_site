from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Question, Tag, QuestionComment, Answer, AnswerComment


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


class QuestionCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].required = False

    class Meta:
        model = QuestionComment
        fields = ('body',)
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='comment_config'
            )
        }


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].required = False

    class Meta:
        model = Answer
        fields = ('body',)
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='comment_config'
            )
        }


class AnswerCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].required = False

    class Meta:
        model = AnswerComment
        fields = ('body',)
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='comment_config'
            )
        }
