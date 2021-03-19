from django import forms
from posts.models import Post, Comment

class PostModelForm(forms.ModelForm):
    body = forms.CharField(label='content',widget=forms.Textarea(attrs={'rows':2}))

    class Meta:
        model = Post
        fields = ('body','picture')

class CommentModelForm(forms.ModelForm):
    comment = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder':'Add a comment...','rows':1}))

    class Meta:
        model = Comment
        fields = ('comment',)