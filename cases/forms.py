from django.forms import ModelForm, CheckboxSelectMultiple, CharField
from django import forms

from django.utils.translation import gettext_lazy as _

from PIL import Image

from .models import *

class CaseImageForm(ModelForm):
    image = forms.ImageField()
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size_kb = 256  # Max size in kilobytes
            if image.size > max_size_kb *1024:
                raise forms.ValidationError(f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_kb} کیلوبایت باشد. حجم فایل شما، {round(image.size/1024, 1)} کیلوبایت است.")  
        return image
    class Meta:
        model = ImageCase
        exclude = ("case", "verified", "visible")


class ImageCaseEditForm(ModelForm):
    image = forms.ImageField()
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size_kb = 256  # Max size in kilobytes
            if image.size > max_size_kb *1024:
                raise forms.ValidationError(f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_kb} کیلوبایت باشد. حجم فایل شما، {round(image.size/1024, 1)} کیلوبایت است.")  
        return image
    class Meta:
        model = ImageCase
        exclude = ("case", "verified", "visible",)

class CasePubForm(ModelForm):
    class Meta:
        fields = ("visible",)
        model=Case
        labels = {
            'visible': ('نمایش عمومی'),
        }
        help_texts={
            'visible': ('خوش‌حال می‌شویم اگر شرح‌حال خود را پس از کامل شدن برای همه به نمایش بگذارید تا از آن بهره ببرند. به یاد داشته باشید که هر شرح‌حالی ارزش خوانده شدن دارد و با درس‌هایی که از آن می‌گیرید می‌توانید به مرور پیشرفت کنید.'),
        }

class FreeGraphForm(ModelForm):
    class Meta:
        model = LabGraphSelection
        exclude = ("case", "author")

class GraphUpdateForm(ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "dir": "rtl",
            }
        )
    )
    class Meta:
        model=LabGraphSelection
        exclude=("author", "case")


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
            "suggests",
        )
        labels = {
            'tags': ('دسته‌بندی تظاهرات'),
            'rts':('بخش'),
        }
        help_texts={
            'tags': ('دسته‌بندی بر اساس تظاهر بالینی اولیه. می‌توانید چند مورد را انتخاب کنید.'),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

class PicassoCreateForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "markdown_editor",
                "id": "md_text_editor",
            }
        )
    )

    image = forms.ImageField()
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size_mb = 1  # Max size in megabytes
            if image.size > max_size_mb * 1024*1024:
                raise forms.ValidationError(f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_mb} مگابایت باشد. حجم فایل شما، {round(image.size/1024**2, 1)} مگابایت است.")  
        img = Image.open(image)
        width, height = img.size
        if width != height:
            raise forms.ValidationError("تصویری که آپلود کرده‌اید، مربعی نیست.")
        elif width<100:
            raise forms.ValidationError("تصویری که برگزیده‌اید بسیار کوچک است.")
        return image

    class Meta:
        model = Picasso
        fields = ["title", "image", "description", "text", "slug", "case", "inappropriate"]
        help_texts={
            'image': ('تصویر شما باید ابعاد مربعی داشته و حجم آن کمتر از یک مگابایت باشد.'),
        }


class PicassoUpdateForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "markdown_editor",
                "id": "md_text_editor",
            }
        )
    )
    
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size_mb = 1  # Max size in megabytes
            if image.size > max_size_mb * 1024*1024:
                raise forms.ValidationError(f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_mb} مگابایت باشد. حجم فایل شما، {round(image.size/1024**2, 1)} مگابایت است.")  
        img = Image.open(image)
        width, height = img.size
        if width != height:
            raise forms.ValidationError("تصویری که آپلود کرده‌اید، مربعی نیست.")
        elif width<100:
            raise forms.ValidationError("تصویری که برگزیده‌اید بسیار کوچک است.")
        return image

    class Meta:
        model = Picasso
        help_texts={
            'image': ('تصویر شما باید ابعاد مربعی داشته و حجم آن کمتر از یک مگابایت باشد.'),
        }
        exclude = (
            "visible",
            "done",
            "slug",
            "verified",
            "premium",
            "rating",
            "lang",
            "choice",
            "author",
            "delete",
            "editors_review",
            "suggests",
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
            "suggests",
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
            "suggests",
        )


# class FollowUpForm(ModelForm):
#     class Meta:
#         model = FollowUp
#         fields = ('date',"text",)


class CaseCreateForm(ModelForm):
    slug=forms.SlugField(widget=forms.TextInput(
        attrs={"autocapitalize":"off"}
    ))
    class Meta:
        model = Case
        exclude = (
            "verified",
            "author",
            "rating",
            "lang",
            "cover",
            "choice",
            "done",
            "visible",
            "premium",
            "suggests",
        )
        labels = {
            'tags': ('دسته‌بندی تظاهرات'),
            'rts':('بخش'),
        }
        help_texts={
            'tags': ('دسته‌بندی بر اساس تظاهر بالینی اولیه. می‌توانید چند مورد را انتخاب کنید.'),
        }
