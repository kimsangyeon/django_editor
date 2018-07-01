from django import forms
from .models import Post, UploadFileModel

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