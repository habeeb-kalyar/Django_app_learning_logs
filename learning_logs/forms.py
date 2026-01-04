from django import forms
from .models import Topic, Entry
class TopicForm(forms.ModelForm):
    """Form for adding a new topic."""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''} # No label for the text 
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # A widget overrides the default HTML input.
        # We want a larger text area (80 columns wide), not a small single-line box.
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
        