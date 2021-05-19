from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='摘要', required=False, )
    # content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)
    content = forms.CharField(widget=CKEditorUploadingWidget, label='正文', required=True)

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title', 'content', 'status'
        )
