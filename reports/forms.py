from django import forms
from .models import AnonymousReport

class ReportForm(forms.ModelForm):
    class Meta:
        model = AnonymousReport
        fields = ['subject', 'content', 'attachment']
