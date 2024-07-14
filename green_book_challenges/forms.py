from django import forms

class ChallengeForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    challenge = forms.CharField(label='Challenge', widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        # Add any validation logic here if needed
        return title

    def clean_challenge(self):
        challenge = self.cleaned_data['challenge']
        # Add any validation logic here if needed
        return challenge
