from django.conf import settings
from django.db import models
from django.urls import reverse


class Case(models.Model):
    verified=models.BooleanField(default=False, )
    rating=models.SmallIntegerField(choices=[("1",1),("2",2),("3",3),("4",4),("5",5)], null=True, blank=True)
    slug = models.SlugField(
        ("Link"),
        max_length=40,
        null=False,
        blank=False,
        unique=True,
        help_text="لینک مورد علاقه برای کیس خود را وارد کنید. تلاش کنید لینکتان گویا و دقیق باشد، پس از این توانایی تغییر آن را نخواهید داشت. استفاده از فاصله (Space) مجاز نیست.",
    )

    rts=[("ریه","ریه"),
         ("هماتولوژی و انکولوژی","هماتولوژی و انکولوژی"),
         ("روماتولوژی","روماتولوژی"),
        ( "غدد","غدد"),
        ("گوارش","گوارش"),
        ("نفرولوژی","نفرولوژی"),
        ("جنرال","جنرال"),
        ("قلب","قلب"),
        ( "پوست","پوست"),
        ( "اطفال","اطفال"),
        ( "زنان","زنان"),
         ("اعصاب","اعصاب"),
        ( "روان","روان"),
         ("ENT","ENT"),
        ( "عفونی","عفونی"),
         ("چشم","چشم"),
         ("مسمومین","مسمومین"),]

    title = models.CharField(("عنوان:"),
        max_length=50,
        null=False,
        blank=False,
    )
    cat=models.CharField(
        ("دسته:"),
        max_length=100,
        choices=rts,
        null=True,
        blank=True,

    )


    description = models.CharField(("توضیح:"),
        max_length=200,
        null=True,
        blank=True,
        help_text="خلاصه‌ای برای نشان دادن در صفحۀ اصلی که می‌تواند از عنوان طولانی‌تر باشد (تا دویست حرف)."
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    pretext = models.TextField(("پیش‌متن"),null=True, blank=True,help_text="اگر خواستید، می‌توانید مقدمه‌ای دربارۀ شرح‌حال خود بنویسید.")

    gender = models.CharField(("جنسیت"),
        max_length=5,
        choices=[("آقا", "Male"), ("خانم", "Female"), ("دیگر", "Other")],
        null=False,
        blank=False,
        default="O",
    )
    location = models.CharField(("محل زندگی"),
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
    job = models.CharField(("پیشه (شغل)"),max_length=20, null=True, blank=True)
    dwelling = models.CharField(("محل زندگی"),max_length=20, null=True, blank=True)
    age = models.PositiveSmallIntegerField(("سن"),null=False, blank=False, default=40)
    marriage = models.CharField(("وضعیت تاهل"),
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
    doctor = models.CharField(("پزشک درمانگر"),max_length=20, null=True, blank=True)
    source = models.CharField(("منبع شرح حال"),max_length=10, null=True, blank=True)
    reliability = models.CharField(("میزان قابل اعتماد بودن بیمار از 5"),
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
    setting = models.CharField(("مرکز درمانی"),max_length=30, null=True, blank=True)

    PR = models.DecimalField(
        max_digits=3, decimal_places=0, null=True, blank=True, default=70
    )
    BP_S = models.DecimalField(
        ("Systolic BP"),
        max_digits=3,
        decimal_places=0,
        null=True,
        blank=True,
        default=120,
        help_text="می‌توانید با حذف کردن مقدار پیش‌فرض، آن را خالی بگذارید.",
    )
    BP_D = models.DecimalField(
        ("Diastolic BP"),
        max_digits=3,
        decimal_places=0,
        null=True,
        blank=True,
        default=80,
        help_text="می‌توانید با حذف کردن مقدار پیش‌فرض، آن را خالی بگذارید.",
    )
    RR = models.DecimalField(
        max_digits=2, decimal_places=0, null=True, blank=True, default=18,
        help_text="می‌توانید با حذف کردن مقدار پیش‌فرض، آن را خالی بگذارید.",
    )
    SPO2_O = models.DecimalField(
        ("SPO2 With Oxygen"),
        max_digits=3,
        decimal_places=0,
        null=True,
        blank=True,
        help_text="می‌توانید با حذف کردن مقدار پیش‌فرض، آن را خالی بگذارید.",
    )
    SPO2_N = models.DecimalField(
        ("SPO2 Without Oxygen"),
        max_digits=3,
        decimal_places=0,
        null=True,
        blank=True,
        help_text="می‌توانید با حذف کردن مقدار پیش‌فرض، آن را خالی بگذارید.",
    )
    Temp = models.DecimalField(
        ("Temperature"),
        max_digits=2,
        decimal_places=0,
        null=True,
        blank=True,
        default=37,
        help_text="می‌توانید با حذف کردن مقدار پیش‌فرض، آن را خالی بگذارید.",
    )

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
    phe = models.TextField(
        ("معاینۀ فیزیکی و بررسی دستگاه‌ها"),
        null=True,
        blank=True,
    )
    dat = models.TextField(
        ("داده‌های پاراکلینیکی"),
        null=True,
        blank=True,
        help_text=("داده‌های آزمایشگاهی و گزارش‌های تصویربرداری، اکوگرافی، نوار قلب و ..."),
    )
    summary = models.TextField(("خلاصۀ شرح حال و معاینه"),
        null=True,
        blank=True,
    )
    ddx= models.TextField(
        ("تشخیص‌های افتراقی"),
        null=True,
        blank=True,
        help_text=("دلیل رد تشخیص‌ها و اقدام‌ها جهت رسیدن به تشخیص قطعی را هم می‌توانید اینجا ذکر کنید."))

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

    post_text= models.TextField(
        ("توضیح پایانی"),
        null=True,
        blank=True,
        help_text=("می‌توانید توضیحات بیشتر که در شرح‌حال قرار نمی‌گیرند و همچنین اطلاعات بیشتر دربارۀ بیماری را در اینجا ذکر کنید."))



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("case_detail", args=[str(self.slug)])


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
    text = models.TextField(("Note"), null=False, blank=False, help_text="توجه کنید که نت‌ها در حال حاضر، قابل تغییر یا پاکسازی نیستند.")
    
    def get_absolute_url(self):
        return reverse("cases_list",kwargs={"slug": self.slug})
    
    def __str__(self):
        return (str(self.date)+" "+self.text[:32])

class Comment(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    verified=models.BooleanField(default=True)
    comment = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.comment[:32]

