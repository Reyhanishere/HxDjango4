from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils.timezone import now
from django.conf import settings
from django.db import models
from django.urls import reverse

class Choice(models.Model):
    name = models.CharField(max_length=36)

    def __str__(self):
        return self.name

class Suggest(models.Model):
    name=models.CharField(max_length=15,null=False, blank=False)
    slug=models.SlugField(null=False, blank=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Rotation(models.Model):
    name=models.CharField(max_length=25)
    slug = models.SlugField(unique=True)
    cover= models.ImageField(upload_to="cases/uploads/", null=True, blank=True)
    def __str__(self):
        return self.name

class Review(models.Model):
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(
        ("متن"),
        default="",
        blank=False,
        null=False,
    )
    
    def __str__(self):
        return f"{self.author}: {self.content_object.title}"
    
class Case(models.Model):
    choice = models.ManyToManyField(Choice, "Choice",null=True, blank=True)
    premium = models.BooleanField(default=False)
    verified = models.BooleanField(
        default=True,
    )
    visible = models.BooleanField(
        default=True,
    )
    done = models.BooleanField(
        default=True,
    )
    
    rating = models.SmallIntegerField(
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, blank=True
    )
    lang = models.CharField(
        ("زبان"),
        max_length=2,
        choices=[("Fa", "Fa")],
        null=False,
        blank=False,
        default="Fa",
    )
    cover = models.ImageField(
        upload_to="cases/hx/uploads/%Y%m%d/", null=True, blank=True
    )

    title = models.CharField(
        ("عنوان:"),
        max_length=50,
        null=False,
        blank=False,
    )
    rts = models.ForeignKey(Rotation, on_delete=models.CASCADE, null=True, blank=True,)

    description = models.CharField(
        ("توضیح:"),
        max_length=200,
        null=True,
        blank=True,
        help_text="خلاصه‌ای برای نشان دادن در صفحۀ اصلی که می‌تواند از عنوان طولانی‌تر باشد (تا دویست حرف).",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    pretext = models.TextField(
        ("پیش‌متن"),
        null=True,
        blank=True,
        help_text="اگر خواستید، می‌توانید مقدمه‌ای دربارۀ شرح‌حال خود بنویسید.",
    )
    is_pedi=models.BooleanField(("آیا کیس کودک است؟"),default=False)

    gender = models.CharField(
        ("جنسیت"),
        max_length=5,
        choices=[("آقا", "Male"), ("خانم", "Female"), ("دیگر", "Other")],
        null=False,
        blank=False,
        default="O",
    )
    location = models.CharField(
        ("مکان مراجعه"),
        max_length=10,
        choices=[
            ("مطب", "مطب"),
            ("درمانگاه", "درمانگاه"),
            ("اورژانس", "اورژانس"),
            ("بخش", "بخش"),
        ],
        null=False,
        blank=False,
        default="بخش",
    )
    job = models.CharField(("پیشه (شغل)"), max_length=20, null=True, blank=True, default="",)
    dwelling = models.CharField(("محل زندگی"), max_length=20, null=True, blank=True, default="")
    age = models.PositiveSmallIntegerField(("سن به سال"), null=False, blank=False, default=40)
    age_m= models.PositiveSmallIntegerField(("باقی سن به ماه"), null=False, blank=False, default=0)
    marriage = models.CharField(
        ("وضعیت تاهل"),
        max_length=15,
        choices=[
            ("متاهل", "متاهل"),
            ("مجرد", "مجرد"),
            ("همسر فوت شده", "همسر فوت شده"),
            ("جداشده", "جداشده"),
        ],
        null=True,
        blank=True,
        default="متاهل"
    )

    source = models.CharField(("منبع شرح حال"), max_length=20, null=True, blank=True, default="")
    reliability = models.CharField(
        ("میزان قابل اعتماد بودن بیمار از 5"),
        max_length=1,
        choices=[
            ("5", "5/5"),
            ("4", "4/5"),
            ("3", "3/5"),
            ("2", "2/5"),
            ("1", "1/5"),
        ],
        null=True,
        blank=True,
    )

    cc = models.CharField(
        ("شکایت اصلی"), max_length=100, null=False, blank=False, default="", help_text="Chief Complaint"
    )
    pi = models.TextField(("شرح بیماری فعلی"), null=False, blank=False, default="", help_text="Present Illness")
    pmh = models.TextField(
        ("شرح بیماری‌های گذشته"),
        null=True,
        blank=True,
        help_text="Past Medical History"
    )
    drg = models.TextField(
        ("داروها"),
        null=True,
        blank=True,
    )
    sh = models.TextField(
        ("شرح حال اجتماعی"),
        null=True,
        blank=True,
        help_text="مصرف مواد مخدر، الکل، وضعیت نظام وظیفه، شغل، روابط اجتماعی و جنسی و ...",
    )
    fh = models.TextField(
        ("سابقۀ بیماری‌های خانواده"),
        null=True,
        blank=True,
        help_text="Family History"
    )
    alg = models.CharField(
        ("حساسیت‌ها"),
        max_length=100,
        null=True,
        blank=True,
    )
    ros = models.TextField(
        ("بررسی دستگاه‌ها"),
        null=True,
        blank=True,
        help_text="Review of Systems"
    )
    phe = models.TextField(
        ("معاینۀ بدنی"),
        null=True,
        blank=True,
        help_text="Physical Examinations"

    )
    dat = models.TextField(
        ("دیگر داده‌ها"),
        null=True,
        blank=True,
        help_text=(
            "داده‌های آزمایشگاهی و گزارش‌های تصویربرداری، اکوگرافی، نوار قلب و ..."
        ),
    )
    summary = models.TextField(
        ("خلاصۀ شرح حال و معاینه"),
        null=True,
        blank=True,
    )
    ddx = models.TextField(
        ("تشخیص‌های افتراقی"),
        null=True,
        blank=True,
        help_text=(
            "دلیل رد تشخیص‌ها و اقدام‌ها جهت رسیدن به تشخیص قطعی را هم می‌توانید اینجا ذکر کنید."
        ),
    )

    act = models.TextField(
        ("اقدامات"),
        null=True,
        blank=True,
    )

    pdx = models.CharField(
        ("تشخیص اولیه"),
        max_length=100,
        null=True,
        blank=True,
    )

    post_text = models.TextField(
        ("توضیح پایانی"),
        null=True,
        blank=True,
        help_text=(
            "می‌توانید توضیحات بیشتر که در شرح‌حال قرار نمی‌گیرند و همچنین اطلاعات بیشتر دربارۀ بیماری را در اینجا ذکر کنید."
        ),
    )

    tags = models.ManyToManyField(Tag, null=True, blank=True,help_text="هم می‌توانید خالی بگذارید و هم می‌توانید چند مورد را انتخاب کنید (با نگه‌داشتن Ctrl در ویندوز).")
    suggests=models.ManyToManyField(Suggest, null=True, blank=True,help_text="هم می‌توانید خالی بگذارید و هم می‌توانید چند مورد را انتخاب کنید (با نگه‌داشتن Ctrl در ویندوز).")
    slug = models.SlugField(
        ("لینک"),
        unique=True,
        max_length=40,
        null=False,
        blank=False,
        help_text="لینک مورد علاقه برای کیس خود را وارد کنید. تلاش کنید لینکتان گویا و دقیق باشد، پس از این توانایی تغییر آن را نخواهید داشت. استفاده از فاصله (Space) مجاز نیست.",
    )
    def sex_pedi(self):
        if self.is_pedi:
            if self.gender=='آقا':
                return "پسر"
            elif self.gender=='آقا':
                return "دختر"
            else:
                return self.gender
        else:
            return self.gender
    
    def get_age(self):
        if self.age > 5:
            return f"{self.age} ساله"
        elif self.age == 0:
            return f"{self.age_m} ماهه"
        elif self.age_m ==0:
            return f"{self.age} ساله"
        else:
            return f"{self.age} سال و {self.age_m} ماهه"
        
    def save(self, *args, **kwargs):
        if not self.pk:
            today = now().strftime('%y%m%d')
            count = Case.objects.filter(date_created__date=now().date()).count() + 1
            self.slug = f"{today}{count:02}"
            while Case.objects.filter(slug=self.slug).exists():
                count += 1
                self.slug = f"{today}{count:02}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("hx_detail", args=[str(self.slug)])

class FollowUp(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date = models.DecimalField(
        ("Days After Admission:"),
        max_digits=2,
        decimal_places=0,
        null=False,
        blank=False,
        default=0,
    )
    text = models.TextField(
        ("Note"),
        null=False,
        blank=False,
        help_text="توجه کنید که نت‌ها در حال حاضر، قابل تغییر یا پاکسازی نیستند.",
    )

    def get_absolute_url(self):
        return reverse("cases_list", kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.date) + " " + self.text[:32]


class Comment(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    verified = models.BooleanField(default=True)
    comment = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    related_name = "comments"
    likes = models.SmallIntegerField(default=0)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')
    def __str__(self):
        return self.comment[:32]

    

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verified = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author.username} in {self.comment.case} to {self.comment.author.username}: {self.content[:50]}"
    

def user_directory_path_hx(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "cases/hx/uploads/hx_{0}/{1}".format(instance.case.author.username, filename)

class ImageCase(models.Model):
    type_choices = [
        ("ECG", "ECG"),
        ("X-Ray", "X-Ray"),
        ("MRI", "MRI"),
        ("Ultra-Sound", "Ultra-Sound"),
        ("CT Scan", "CT Scan"),
        ("Other", "Other"),
    ]
    verified=models.BooleanField(default=True)
    visible=models.BooleanField(default=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    related_name = "imagecase"
    image = models.ImageField(
        "آپلود تصویر", upload_to=user_directory_path_hx, null=False, blank=False
    )
    type = models.CharField(
        "نوع داده",
        choices=type_choices,
        default="Other",
        max_length=16,
        null=False,
        blank=False,
    )

    text = models.TextField(
        "متن",
        help_text="توضیح یا گزارش تصویر",
        blank=True,
        null=True,
    )
    def __str__(self):
        return f"{self.case.slug}: {self.type}"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "cases/picasso/uploads/user_{0}/{1}".format(instance.author.username, filename)


class Picasso(models.Model):
    choice = models.ManyToManyField(Choice, null=True, blank=True)
    premium = models.BooleanField(default=False)
    verified = models.BooleanField(default=True)
    visible = models.BooleanField(
        default=True,
    )
    done = models.BooleanField(
        default=True,
    )
    delete=models.BooleanField("I want to DELETE this Picasso.",
        default=False,
    )
    lang = models.CharField(max_length=2, choices=[("Fa", "Fa")], default="Fa")
    rating = models.SmallIntegerField(
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, blank=True
    )
    title = models.CharField(
        ("عنوان"),
        max_length=50,
        help_text="برای نشان دادن در صفحۀ اصلی.",
        blank=False,
        null=False,
    )
    image = models.ImageField(upload_to=user_directory_path, null=False, blank=False)
    description = models.CharField(
        ("توضیح کوتاه"),
        max_length=200,
        help_text="خلاصه‌ای برای نمایش در صفحۀ اصلی",
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        ("لینک"),
        unique=True,
        help_text="برای دسترسی به این تصویر یک آدرس مرتبط ایجاد کنید. برای مثال cushing-striae-01.",
        blank=False,
        null=False,
    )
    text = models.TextField(
        ("متن"),
        help_text="متنی کامل دربارۀ تصویر بنویسید. دربارۀ بیماری، دلیل ایجاد این وضعیت و تمام موارد مرتبط.",
        default="",
        blank=False,
        null=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    tags=models.ManyToManyField(Tag, null=True, blank=True)
    inappropriate=models.BooleanField(("آزاردهنده"),default=False,help_text="اگر این تصویر می‌تواند برای بخشی از جامعۀ هدف آزاردهنده باشد، این تیک را بزنید تا به طور واضح در صفحۀ نخست سایت به نمایش در نیاید.")
    case = models.URLField(
        "لینک کیس مرتبط",
        help_text="می‌توانید لینک کیس مربوط به این تصویر را در اینجا قرار دهید.",
        null=True,
        blank=True,
    )
    editors_review=models.TextField(blank=True,null=True)
    suggests=models.ManyToManyField(Suggest, null=True, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("picasso_detail", args=[str(self.slug)])

    # def save(self, *args, **kwargs):
    #     if not self.verified:
    #         pass
    #     else:
    #         if self.slug:  # Check if the instance has already been saved
    #             old_instance = Picasso.objects.get(slug=self.slug)
    #             # Check if the image field has changed
    #             if old_instance.image != self.image:
    #                 self.verified = False  # Set verified to False if image has changed
    #         else:  # New instance is being created
    #             self.verified = False  # Set verified to False for new instances

    #     # Call the parent class's save method to save the instance
    #     super(Picasso, self).save(*args, **kwargs)

class Note(models.Model):
    choice = models.ManyToManyField(Choice, null=True, blank=True)
    premium = models.BooleanField(default=False)
    verified = models.BooleanField(default=True)
    visible = models.BooleanField(
        default=True,
    )
    done = models.BooleanField(
        default=True,
    )
    lang = models.CharField(max_length=2, choices=[("Fa", "Fa")], default="Fa")
    rating = models.SmallIntegerField(
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, blank=True
    )
    title = models.CharField(
        ("عنوان"),
        max_length=50,
        help_text="برای نشان دادن در صفحۀ اصلی.",
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        ("توضیح کوتاه"),
        max_length=200,
        help_text="خلاصه‌ای برای نمایش در صفحۀ اصلی",
        blank=False,
        null=False,
    )
    text = models.TextField(
        ("متن"),
        help_text="اینجا در اختیار شماست تا تمام متن خود را بنویسید.",
        default="",
        blank=False,
        null=False,
    )
    
    tags=models.ManyToManyField(Tag, null=True, blank=True)
    slug = models.SlugField(
        ("لینک"),
        unique=True,
        help_text="برای دسترسی به این یادداشت یک آدرس مرتبط ایجاد کنید. برای مثال ems-01.",
        blank=False,
        null=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    
    delete = models.BooleanField("I want to DELETE this Ex.",
        default=False,
    )
    editors_review=models.TextField(blank=True,null=True)

    suggests=models.ManyToManyField(Suggest, null=True, blank=True)

    def __str__(self):
        return self.title

class LabGraphSelection(models.Model):   
    title = models.CharField(
        max_length=64,
        help_text="You can name this selection.",
        blank=False,
        null=False,
    )
    case=models.ForeignKey(Case, on_delete=models.CASCADE, blank=True, null=True)
    data=models.TextField(blank=False, null=False)
    description=models.TextField(help_text="Optional", blank=True, null=True)
    zero=models.BooleanField(("رسم از صفر"),default=False,help_text="اگر می‌خواهید عدد صفر هم در نمودار درج شود، این تیک را بزنید")
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.case:
            return str(self.title) + " from " + str(self.case) + " by " + str(self.author)
        else:
            return str(self.title) + " FREE by " + str(self.author)

class AIReqResLog(models.Model):
    AI_MODELS=[        
        ("CC", "CC" ),
        ("PI", "PI" ),
        ("ROS", "ROS" ),
        ("PhE", "PhE" ),
        ("Sum", "Sum" ),
        ("DDx", "DDx" ),
        ("Act", "Act" ),
        ]
    request_content=models.TextField(blank=False, null=False)
    response_content=models.TextField(blank=False, null=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ai_model = models.CharField(
        max_length=10,
        choices=AI_MODELS,
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f"{self.ai_model}: {self.request_content[:20]} | {self.response_content[:20]} by {self.user.username}"
