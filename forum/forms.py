from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Question

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].required = False

    class Meta:
        model = Question
        fields = ('title', 'body')
        widgets = {
            "body": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="body_config"
            )
        }