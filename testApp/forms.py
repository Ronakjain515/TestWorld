from django import forms
from .models import TalkToUs

class TalkToUsForm(forms.ModelForm):
    class Meta:
        model = TalkToUs
        fields = ["name", "email", "message"]