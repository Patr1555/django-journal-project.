from django import forms
from .models import JournalEntry

class JournalEntryForm(forms.ModelForm):
    
    #ModelForm automatically creates form fields for the model fields.
    #Using a ModelForm avoids hand-coding inputs for title, content, image.

    class Meta:
     model=JournalEntry  # the model the form is based on
     fields=['title','content','image']# fields the user can edit/upload


    