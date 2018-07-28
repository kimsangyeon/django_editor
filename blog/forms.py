from django import forms
from .models import Post, Page, UploadFileModel
from froala_editor.widgets import FroalaEditor

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('contents',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ('file', 'extension')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False