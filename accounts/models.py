from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    FIELDS = [
        ("MD", "MD/Student" ),
        ("Dent", "Dentist/Student" ),
        ("Nurse", "Nurse/Student" ),
        ("Other", "Other" ),
        ("NMS", "Not Medical Science" ),
    ]
    DEGREES = [
        ("Basic Sciences", "Basic Sciences"),
        ("Pathophysiology", "Pathophysiology"),
        ("Medical Extern", "Medical Extern"),
        ("Medical Intern", "Medical Intern"),
        ("General Practicioner", "General Practicioner"),
        ("Medical Resident", "Medical Resident"),
        ("Medical Specialist", "Medical Specialist"),
        ("Fellowship", "Fellowship"),
        ("Superspecialist", "Superspecialist"),
        # " ", "-None-",
    ]
    UNIS = [
        ("MUMS", "علوم پزشکی مشهد" ),
        ("TUMS", "علوم پزشکی تهران" ),
        ("NKUMS", "علوم پزشکی خراسان شمالی" ),
        (
            "SBMU", "علوم پزشکی بهشتی",
        ),
        ("SUMS", "علوم پزشکی شیراز" ),
        ("IUMS", "علوم پزشکی ایران" ),
        ("MedIAU", "دانشگاه آزاد"),
        ("MUI", "علوم پزشکی اصفهان" ),
        ("GOUMS", "علوم پزشکی گرگان" ),
        ("GUMS", "علوم پزشکی گیلان" ),
        ("TBZMed", "علوم پزشکی تبریز" ),
        ("MazUMS", "علوم پزشکی ساری" ),
        ("MUBabol", "علوم پزشکی بابل" ),
        ("AJUMS", "علوم پزشکی جندی‌شاپور اهواز" ),
        ("BMSU", "علوم پزشکی بقیة‌الله" ),
        ("KMU", "علوم پزشکی کرمان" ),
        ("UMSU", "علوم پزشکی ارومیه" ),
        ("UMSHa", "علوم پزشکی همدان" ),
        ("MedSab", "علوم پزشکی سبزوار" ),
        ("BPUMS", "علوم پزشکی بوشهر" ),
        ("SemUMS", "علوم پزشکی سمنان" ),
        ("HUMS", "علوم پزشکی هرمزگان" ),
        ("KUMS", "علوم پزشکی کرمانشاه" ),
        ("ABZUMS", "علوم پزشکی البرز" ),
        ("BUMS", "علوم پزشکی بیرجند" ),
        ("ZUMS", "علوم پزشکی زابل" ),
        ("ZAUMS", "علوم پزشکی زاهدان" ),
        ("SSU", "علوم پزشکی یزد" ),
        ("SKUMS", "علوم پزشکی شهرکرد" ),
        ("ShMU", "علوم پزشکی شاهرود" ),
        ("NUMS", "علوم پزشکی نیشابور" ),
        ("YUMS", "علوم پزشکی یاسوج" ),
        ("LUMS", "علوم پزشکی لرستان" ),
        ("MUK", "علوم پزشکی کردستان" ),
        ("MUQ", "علوم پزشکی قم" ),
        ("QUMS", "علوم پزشکی قزوین" ),
        ("----", "Other" ),
    ]
    # , help_text="بهتر است به فارسی بنویسید."
    first_name = models.CharField(
        max_length=50,
    )
    last_name = models.CharField(max_length=50)
    field = models.CharField(
        max_length=32,
        choices=FIELDS,
        null=False,
        blank=True,
    )
    degree = models.CharField(
        max_length=20,
        choices=DEGREES,
        null=True,
        blank=True,
        help_text=("Your current degree. Leave empty if not Medical Doctor/Student."),
    )

    university = models.CharField(
        max_length=30,
        choices=UNIS,
        null=True,
        blank=True,
        help_text=("Your current university. Leave empty if not a student."),
    )
    is_article_author = models.BooleanField(default=False, blank=False, null=False)
    is_article_editor = models.BooleanField(default=False, blank=False, null=False)
    is_case_editor = models.BooleanField(default=False, blank=False, null=False)

    fn_fa = models.CharField("نام به فارسی", max_length=50, blank=True, null=True)
    ln_fa = models.CharField(
        "نام خانوادگی به فارسی", max_length=50, blank=True, null=True
    )
    about_me = models.TextField(
        "دربارۀ من",
        blank=True,
        null=True,
    )
    en_name= models.BooleanField(default=True)

    hx_cc_ai_permission=models.BooleanField(default=False)
    hx_cc_ai_use_count=models.PositiveIntegerField(default=0)

    hx_pi_ai_permission=models.BooleanField(default=False)
    hx_pi_ai_use_count=models.PositiveIntegerField(default=0)
    
    hx_ros_ai_permission=models.BooleanField(default=False)
    hx_ros_ai_use_count=models.PositiveIntegerField(default=0)

    hx_phe_ai_permission=models.BooleanField(default=False)
    hx_phe_ai_use_count=models.PositiveIntegerField(default=0)

    hx_sum_ai_permission=models.BooleanField(default=False)
    hx_sum_ai_use_count=models.PositiveIntegerField(default=0)
    
    hx_ddx_ai_permission=models.BooleanField(default=False)
    hx_ddx_ai_use_count=models.PositiveIntegerField(default=0)

    def join_date_day(self):
        return self.date_joined.date()
