from django.forms import ModelForm, CheckboxSelectMultiple, CharField
from django import forms


from .models import (
    Case,
    #  FollowUp,
    Comment,
    Picasso,
)


class CaseUpdateForm(ModelForm):
    class Meta:
        model = Case
        exclude = ("slug", "verified", "author", "rating", "lang", "cover", "choice")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class PicassoCreateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'markdown-editor',
                                                        'id':'picasso-create-text-editor',}))

    class Meta:
        model = Picasso
        fields = ["title", "image", "description", "text", "slug", "case"]


class PicassoUpdateForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'markdown-editor',
                                                        'id':'picasso-edit-text-editor',}))
    class Meta:
        model = Picasso
        exclude = ("slug", "verified", "premium", "rating", "lang", "choice", "author")


# class FollowUpForm(ModelForm):
#     class Meta:
#         model = FollowUp
#         fields = ('date',"text",)


# class CaseCreateForm(ModelForm):
#     class Meta:
#         model = Case
#         exclude = ("author",)
