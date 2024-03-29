from django.conf import settings
from django.db import models
from django.urls import reverse


# class Choice(models.Model):
#     name = models.CharField(max_length=36)

#     def __str__(self):
#         return self.name


# class Tag(models.Model):
#     name = models.CharField(max_length=16)
#     slug = models.SlugField()

#     def __str__(self):
#         return self.name


class Case(models.Model):
    # chice = models.ManyToManyField(Choice, "Choice",null=True, blank=True)
    verified = models.BooleanField(
        default=False,
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
    slug = models.SlugField(
        ("Link"),
        max_length=40,
        null=False,
        blank=False,
        unique=True,
        help_text="لینک مورد علاقه برای کیس خود را وارد کنید. تلاش کنید لینکتان گویا و دقیق باشد، پس از این توانایی تغییر آن را نخواهید داشت. استفاده از فاصله (Space) مجاز نیست.",
    )
    cover = models.ImageField(
        upload_to="cases/hx/uploads/%Y%m%d/", null=True, blank=True
    )

    rts = [
        ("ریه", "ریه"),
        ("هماتولوژی و انکولوژی", "هماتولوژی و انکولوژی"),
        ("روماتولوژی", "روماتولوژی"),
        ("غدد", "غدد"),
        ("گوارش", "گوارش"),
        ("نفرولوژی", "نفرولوژی"),
        ("جنرال", "جنرال"),
        ("قلب", "قلب"),
        ("پوست", "پوست"),
        ("اطفال", "اطفال"),
        ("زنان", "زنان"),
        ("اعصاب", "اعصاب"),
        ("روان", "روان"),
        ("ENT", "ENT"),
        ("عفونی", "عفونی"),
        ("چشم", "چشم"),
        ("مسمومین", "مسمومین"),
    ]

    title = models.CharField(
        ("عنوان:"),
        max_length=50,
        null=False,
        blank=False,
    )
    cat = models.CharField(
        ("دسته:"),
        max_length=100,
        choices=rts,
        null=True,
        blank=True,
    )

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
        default="ROT",
    )
    job = models.CharField(("پیشه (شغل)"), max_length=20, null=True, blank=True)
    dwelling = models.CharField(("محل زندگی"), max_length=20, null=True, blank=True)
    age = models.PositiveSmallIntegerField(("سن"), null=False, blank=False, default=40)
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
    )
    # date_of_admission=models.DateField(null=True, blank=True)
    doctor = models.CharField(("پزشک درمانگر"), max_length=20, null=True, blank=True)
    source = models.CharField(("منبع شرح حال"), max_length=10, null=True, blank=True)
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
    setting = models.CharField(("مرکز درمانی"), max_length=30, null=True, blank=True)

    cc = models.CharField(
        ("شکایت اصلی"), max_length=100, null=False, blank=False, default=""
    )
    pi = models.TextField(("شرح بیماری فعلی"), null=False, blank=False, default="")
    pmh = models.TextField(
        ("شرح بیماری‌های گذشته"),
        null=True,
        blank=True,
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
    )
    phe = models.TextField(
        ("معاینۀ بدنی"),
        null=True,
        blank=True,
    )
    dat = models.TextField(
        ("داده‌های پاراکلینیکی"),
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

    # tags = models.ManyToManyField(Tag, null=True, blank=True)
    picasso = models.URLField(
        "لینک کیس مرتبط",
        help_text="می‌توانید لینک کیس مربوط به این تصویر را در اینجا قرار دهید.",
        null=True,
        blank=True,
    )

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

    def __str__(self):
        return self.comment[:32]


class LabTestItem(models.Model):
    cat_choice = [
        ("Blood", "Blood"),
        ("Biochemistry", "Biochemistry"),
        ("U/A", "U/A"),
        ("Serologic", "Serologic"),
        ("Other", "Other"),
    ]
    flg_choice = [
        ("NL", "NL"),
        ("H", "H"),
        ("L", "L"),
        ("Positive", "Positive"),
        ("Negative", "Negative"),
        ("Other", "Other"),
    ]
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    day = models.SmallIntegerField(default=0, null=True, blank=True)
    item_abbr = models.CharField(
        "مخفف نام", help_text="eg: WBC", max_length=16, null=False, blank=False
    )
    item_full = models.CharField(
        "نام کامل",
        help_text="eg: White Blood Cell",
        max_length=50,
        null=True,
        blank=True,
    )
    category = models.CharField(
        "دسته",
        max_length=25,
        choices=cat_choice,
        default="Blood",
        null=False,
        blank=False,
    )
    value = models.CharField("مقدار", default="", max_length=8, null=False, blank=False)
    unit = models.CharField(
        "واحد", default="10^3/µL", max_length=16, null=False, blank=False
    )
    ref_rng = models.CharField(
        "بازۀ مرجع",
        default="",
        help_text="eg: 3.8 - 5.4",
        max_length=16,
        null=False,
        blank=False,
    )
    flag = models.CharField(
        "وضعیت",
        max_length=25,
        choices=flg_choice,
        default="Other",
        null=False,
        blank=False,
    )
    related_name = "lab"

    def __str__(self):
        return self.item_abbr[:32]


def user_directory_path_hx(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "cases/hx/uploads/hx_{0}/{1}".format(instance.case.slug, filename)


class ImageCase(models.Model):
    type_choices = [
        ("ECG", "ECG"),
        ("X-Ray", "X-Ray"),
        ("MRI", "MRI"),
        ("Ultra-Sound", "Ultra-Sound"),
        ("Other", "Other"),
    ]
    verified=models.BooleanField(default=False)
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


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "cases/picasso/uploads/user_{0}/{1}".format(instance.case.username, filename)


class Picasso(models.Model):
    choice = models.ManyToManyField(Choice, null=True, blank=True)
    premium = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
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
    case = models.URLField(
        "لینک کیس مرتبط",
        help_text="می‌توانید لینک کیس مربوط به این تصویر را در اینجا قرار دهید.",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("picasso_detail", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.verified:
            pass
        else:
            if self.slug:  # Check if the instance has already been saved
                old_instance = Picasso.objects.get(slug=self.slug)
                # Check if the image field has changed
                if old_instance.image != self.image:
                    self.verified = False  # Set verified to False if image has changed
            else:  # New instance is being created
                self.verified = False  # Set verified to False for new instances

        # Call the parent class's save method to save the instance
        super(Picasso, self).save(*args, **kwargs)
