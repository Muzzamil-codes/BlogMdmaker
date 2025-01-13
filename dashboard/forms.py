from django import forms
from .models import BlogModel

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['draft', 'content']