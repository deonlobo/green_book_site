from django import forms

from green_book_challenges.models import CompletedTask


class ChallengeForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    task = forms.CharField(label='Task', widget=forms.Textarea)
    image = forms.ImageField(label='Image')
    deadline = forms.DateField(label='Deadline')

    def clean_title(self):
        title = self.cleaned_data['title']
        # Add any validation logic here if needed
        return title

    def clean_task(self):
        task = self.cleaned_data['task']
        # Add any validation logic here if needed
        return task


class CompletedTaskForm(forms.ModelForm):
    class Meta:
        model = CompletedTask
        fields = ['image', 'caption']
