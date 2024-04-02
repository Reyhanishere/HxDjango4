from django.forms import ModelForm, CheckboxSelectMultiple, CharField
from django import forms


from .models import (
    Case,
    #  FollowUp,
    Comment,
    Picasso,
    # LabTestItem,
    ImageCase,
    Note,
)

# LabTestForm = forms.inlineformset_factory(
#     Case, LabTestItem, fields="__all__", extra=1, can_delete=True, can_order=False
# )


class CaseImageForm(ModelForm):
    class Meta:
        model = ImageCase
        exclude = ("case", "verified", "visible")


class CaseUpdateForm(ModelForm):
    class Meta:
        model = Case
        exclude = (
            "slug",
            "verified",
            "author",
            "rating",
            "lang",
            "cover",
            "choice",
            "done",
            "visible",
            "premium",
        )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class PicassoCreateForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "markdown_editor",
                "id": "md_text_editor",
            }
        )
    )

    class Meta:
        model = Picasso
        fields = ["title", "image", "description", "text", "slug", "case"]


class PicassoUpdateForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "markdown_editor",
                "id": "md_text_editor",
            }
        )
    )

    class Meta:
        model = Picasso
        exclude = (
            "slug",
            "verified",
            "premium",
            "rating",
            "lang",
            "choice",
            "author",
            "delete",
            "editors_review",
        )


class ExUpdateForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "markdown_editor",
                "id": "md_text_editor",
            }
        )
    )

    class Meta:
        model = Note
        exclude = (
            "slug",
            "verified",
            "premium",
            "rating",
            "lang",
            "choice",
            "author",
            "delete",
            "editors_review",
            "done",
            "visible",
        )


class ExCreateForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "markdown_editor",
                "id": "md_text_editor",
            }
        )
    )

    class Meta:
        model = Note
        exclude = (
            "verified",
            "premium",
            "rating",
            "lang",
            "choice",
            "author",
            "delete",
            "editors_review",
            "done",
            "visible",
        )


# class FollowUpForm(ModelForm):
#     class Meta:
#         model = FollowUp
#         fields = ('date',"text",)


# class CaseCreateForm(ModelForm):
#     class Meta:
#         model = Case
#         exclude = ("author",)
