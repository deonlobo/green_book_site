from django import forms


class PrivateConversationForm(forms.Form):
    user_name = forms.CharField(
        label="username",
        max_length=150,
        required=True
    )

class GroupConversationForm(forms.Form):
    group_name = forms.CharField(label="group_name", max_length=150, required=True)
    participant_ids = forms.CharField(label="participant_ids", required=True)
    