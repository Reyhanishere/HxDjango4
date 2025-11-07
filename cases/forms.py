from django.forms import ModelForm, CheckboxSelectMultiple, CharField
from django import forms

from django.utils.translation import gettext_lazy as _

from PIL import Image

from .models import *
from accounts.models import ProfessorProfile


class CaseCreateForm(ModelForm):
    cc = forms.CharField.widget=forms.TextInput(attrs={'autocomplete':'off',})
                                                                
    field_order = ["title", "description", "pretext", "location", "is_pedi"]

    class Meta:
        model = Case
        exclude = (
            # "rts",
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
            "slug",
            "is_university_case",
            "is_professor_turn",
            "professor_verified",
            "professor",
            "alg",
            "professor_post_text",
            "cc_tags",
            "dx_tags",
            "tags",
        )

        labels = {
            "tags": ("دسته‌بندی تظاهرات"),
            "rts": ("بخش"),
        }
        help_texts = {
            "tags": (
                "دسته‌بندی بر اساس تظاهر بالینی اولیه. می‌توانید چند مورد را انتخاب کنید."
            ),
        }


class CaseUpdateForm(ModelForm):
    field_order = ["title", "description", "pretext", "location", "is_pedi"]

    class Meta:
        model = Case
        exclude = (
            "slug",
            # "rts",
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
            "is_university_case",
            "is_professor_turn",
            "professor_verified",
            "professor",
            "alg",
            "professor_post_text",
            "cc_tags",
            "dx_tags",
            "tags",
        )
        labels = {
            "tags": ("دسته‌بندی تظاهرات"),
            "rts": ("بخش"),
        }
        help_texts = {
            "tags": (
                "دسته‌بندی بر اساس تظاهر بالینی اولیه. می‌توانید چند مورد را انتخاب کنید."
            ),
        }


class CaseImageForm(ModelForm):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            max_size_kb = 4096  # Max size in kilobytes
            if image.size > max_size_kb * 1024:
                raise forms.ValidationError(
                    f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_kb} کیلوبایت باشد. حجم فایل شما، {round(image.size/1024, 1)} کیلوبایت است."
                )
        return image
    
    def __init__(self, *args, **kwargs):
        self.is_old = kwargs.pop('is_old', None)
        super().__init__(*args, **kwargs)
        if self.is_old != None:
            self.fields['is_old'].widget = forms.HiddenInput()
        

    class Meta:
        model = ImageCase
        exclude = ("case", "verified", "visible",)


class ImageCaseEditForm(ModelForm):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            max_size_kb = 2048  # Max size in kilobytes
            if image.size > max_size_kb * 1024:
                raise forms.ValidationError(
                    f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_kb} کیلوبایت باشد. حجم فایل شما، {round(image.size/1024, 1)} کیلوبایت است."
                )
        return image

    class Meta:
        model = ImageCase
        exclude = (
            "case",
            "verified",
            "visible",
        )


class CasePubForm(ModelForm):
    class Meta:
        model = Case
        fields = ("visible", "author")
        labels = {
            "visible": ("نمایش عمومی"),
        }
        help_texts = {
            "visible": (
                "خوش‌حال می‌شویم اگر شرح‌حال خود را پس از کامل شدن برای همه به نمایش بگذارید تا از آن بهره ببرند. به یاد داشته باشید که هر شرح‌حالی ارزش خوانده شدن دارد و با درس‌هایی که از آن می‌گیرید می‌توانید به مرور پیشرفت کنید."
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CasePubForm, self).__init__(*args, **kwargs)
        self.fields["author"].widget = forms.HiddenInput()

    def clean(self):

        cleaned_data = super().clean()

        # Calculate the current count of objects meeting the criteria
        existing_count = Case.objects.filter(
            author=self.cleaned_data["author"], visible=False
        ).count()

        # Check if the form's visibility change would affect the count
        if self.instance.id:  # If the form is for updating an existing object
            if self.instance.visible and not cleaned_data["visible"]:
                existing_count += (
                    1  # Increment count if visibility is changing from True to False
                )
            elif not self.instance.visible and cleaned_data["visible"]:
                existing_count -= (
                    1  # Decrement count if visibility is changing from False to True
                )

        # Raise a ValidationError if the count exceeds 3
        if existing_count > 3:
            raise forms.ValidationError(
                "شما نمی‌توانید بیش از سه شرح حال در حالت خصوصی داشته باشید. برای تبدیل این شرح حال به حالت خصوصی، ابتدا یک شرح حال دیگر را عمومی کنید."
            )

        return cleaned_data


class FreeGraphForm(ModelForm):
    class Meta:
        model = LabGraphSelection
        exclude = ("case", "author")


class GraphUpdateForm(ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "dir": "auto",
            }
        ),
        required=False,
    )

    class Meta:
        model = LabGraphSelection
        exclude = ("author", "case")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]


### Uni Cases


class CaseCCAndIDForm(forms.ModelForm):
    cc = forms.CharField(required=True,
                        label="شکایت اصلی",
                        help_text="Chief Complaint",
                        widget=forms.TextInput(
                        attrs={
                            'dir': 'auto',
                            'autocomplete':'off',
                        }
                    ))
    
    age = forms.IntegerField(required=True,
                             widget=forms.NumberInput(
                                attrs={
                                    "value": "40",
                                }
                            ))
    
    class Meta:
        model = Case
        fields = [
            "cc",
            "gender",
            "location",
            "job",
            "born_city",
            "dwelling",
            "age",
            "marriage",
            "source",
            "reliability",
        ]

class CasePIForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["pi"]

class CasePMHForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["pmh","previous_data"]

class CaseDSFForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["drg","sh","fh"]
        
class CaseROSPhEForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["ros","phe"]

class CaseLastFieldsForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["summary", "ddx", "act", "dat", "pdx", "fdx"]

class CaseSelectProfForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['professor']

    def __init__(self, *args, **kwargs):
        working_university = kwargs.pop('working_university', None)
        super().__init__(*args, **kwargs)
        if working_university:
            self.fields['professor'].queryset = ProfessorProfile.objects.filter(
                working_university=working_university
            )

class CaseFinalsForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["professor_post_text", "rts", "tags", "cc_tags", "dx_tags", "suggests", 'professor_verified']
        labels = {
            "rts": ("روتیشن / بخش"),
            "cc_tags": ("تگ‌های شکایت اصلی"),
            "dx_tags": ("تگ‌های تشخیص"),
            "tags": ("سایر تگ‌های کیس"),
            "suggests": ("مناسب برایِ"),
            "professor_verified": ("آیا تایید نهایی می‌کنید؟"),
    
        }
        help_texts = {
            "tags": (
                "تمام تگ‌هایی که به نظرتان برای دسته‌بندی کیس مناسب است و در تگ‌های شکایت و تشخیص انتخاب نکردید."
            ),
            "cc_tags": (
                "می‌توانید مواردی که در لیست نیستند را اضافه کنید."
            ),
            "dx_tags": (
                "می‌توانید مواردی که در لیست نیستند را اضافه کنید."
            ),
            "professor_verified": (
                "با تایید نهایی، دانشجو دیگر توان ویرایش این کیس را نخواهد داشت و با تیک تایید شده و به نام شما، در سایت ثبت می‌شود."
            ),
        }
### End of Uni Cases Forms


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
        image = self.cleaned_data.get("image")
        if image:
            max_size_mb = 1  # Max size in megabytes
            if image.size > max_size_mb * 1024 * 1024:
                raise forms.ValidationError(
                    f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_mb} مگابایت باشد. حجم فایل شما، {round(image.size/1024**2, 1)} مگابایت است."
                )
        img = Image.open(image)
        width, height = img.size
        if width != height:
            raise forms.ValidationError("تصویری که آپلود کرده‌اید، مربعی نیست.")
        elif width < 100:
            raise forms.ValidationError("تصویری که برگزیده‌اید بسیار کوچک است.")
        return image

    class Meta:
        model = Picasso
        fields = [
            "title",
            "image",
            "description",
            "text",
            "slug",
            "case",
            "inappropriate",
        ]
        help_texts = {
            "image": (
                "تصویر شما باید ابعاد مربعی داشته و حجم آن کمتر از یک مگابایت باشد."
            ),
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
        image = self.cleaned_data.get("image")
        if image:
            max_size_mb = 1  # Max size in megabytes
            if image.size > max_size_mb * 1024 * 1024:
                raise forms.ValidationError(
                    f"حجم تصویری که بارگذاری می‌کنید نباید بیشتر از {max_size_mb} مگابایت باشد. حجم فایل شما، {round(image.size/1024**2, 1)} مگابایت است."
                )
        img = Image.open(image)
        width, height = img.size
        if width != height:
            raise forms.ValidationError("تصویری که آپلود کرده‌اید، مربعی نیست.")
        elif width < 100:
            raise forms.ValidationError("تصویری که برگزیده‌اید بسیار کوچک است.")
        return image

    class Meta:
        model = Picasso
        help_texts = {
            "image": (
                "تصویر شما باید ابعاد مربعی داشته و حجم آن کمتر از یک مگابایت باشد."
            ),
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
