from django import forms
from django.forms import ModelForm
from notes.models import Note, Tag

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['summary','text','tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }


class NoteSearchForm(forms.Form):

    '''
    Separate form for searching so can make search fields optional wheres in NoteForm used for entry they are required
    If  want to change widget could adjust tags as follows:
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    '''
    search_text = forms.CharField(required=False)
    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    search_tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)      

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']


    


