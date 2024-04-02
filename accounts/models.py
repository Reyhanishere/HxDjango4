from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    FIELDS=[        
        ("MD/Student", "MD"),
        ("Dentist/Student", "Dent"),
        ("Nurse/Student", "Nurse"),
        ("Other", "Other"),
        ("Not Medical Science", "NMS"),
        
]
    DEGREES = [
        ("Basic Sciences", "Basic Sciences"),
        ("Physiopathology", "Physiopathology"),
        ("Medical Extern", "Medical Extern"),
        ("Medical Intern", "Medical Intern"),
        ("General Practicioner", "General Practicioner"),
        ("Medical Resident", "Medical Resident"),
        ("Medical Specialist", "Medical Specialist"),
        ("Fellowship", "Fellowship"),
        ("Superspecialist","Superspecialist"),
        # " ", "-None-",
    ]
    UNIS = [
        ("علوم پزشکی مشهد","MUMS"),
        ( "علوم پزشکی تهران","TUMS"),
        ("علوم پزشکی خراسان شمالی","NKUMS"),
        ("علوم پزشکی بهشتی","SBMU",),
        ("علوم پزشکی شیراز","SUMS"),
        ("علوم پزشکی ایران","IUMS"),
        ("علوم پزشکی اصفهان","MUI"),
        ("علوم پزشکی گرگان","GOUMS"),
        ("علوم پزشکی گیلان","GUMS"),
        ("علوم پزشکی تبریز","TBZMed"),
        ("علوم پزشکی ساری","MazUMS"),
        ("علوم پزشکی بابل","MUBabol"),
        ("علوم پزشکی جندی‌شاپور اهواز","AJUMS"),
        ("علوم پزشکی بقیة‌الله","BMSU"),
        ("علوم پزشکی کرمان","KMU"),
        ("علوم پزشکی ارومیه","UMSU"),
        ("علوم پزشکی همدان","UMSHa"),
        ("علوم پزشکی سبزوار","MedSab"),
        ("علوم پزشکی بوشهر","BPUMS"),
        ("علوم پزشکی سمنان","SemUMS"),
        ("علوم پزشکی هرمزگان","HUMS"),
        ("علوم پزشکی کرمانشاه","KUMS"),
        ("علوم پزشکی البرز","ABZUMS"),
        ("علوم پزشکی بیرجند","ABZUMS"),
        ("علوم پزشکی زابل","ABZUMS"),
        ("علوم پزشکی زاهدان","ABZUMS"),
        ("علوم پزشکی یزد","SSU"),
        ("علوم پزشکی شهرکرد","SKUMS"),
        ("علوم پزشکی شاهرود","ShMU"),
        ("علوم پزشکی نیشابور","NUMS"),
        ("علوم پزشکی یاسوج","YUMS"),
        ("علوم پزشکی لرستان","LUMS"),
        ("علوم پزشکی کردستان","MUK"),
        ("علوم پزشکی قم","MUQ"),
        ("علوم پزشکی قزوین","QUMS"),
        ("Other", "----"),
    ]
    # , help_text="بهتر است به فارسی بنویسید."
    first_name= models.CharField(max_length=50,)
    last_name= models.CharField(max_length=50)
    field=models.CharField(max_length=32, choices=FIELDS, null=False, blank=True,)
    degree = models.CharField(max_length=20, choices=DEGREES, null=True, blank=True,
            help_text=(
            "Your current degree. Leave empty if not Medical Doctor/Student."
        ),)

    university= models.CharField(max_length=30, choices=UNIS, null=True, blank=True,
            help_text=(
            "Your current university. Leave empty if not a student."
        ),)
    is_article_author=models.BooleanField(blank=True, null=True)
    is_article_editor=models.BooleanField(blank=True, null=True)
    is_case_editor=models.BooleanField(blank=True, null=True)

    fn_fa= models.CharField("نام به فارسی",max_length=50,blank=True, null=True)
    ln_fa= models.CharField("نام خانوادگی به فارسی",max_length=50,blank=True, null=True)
    about_me=models.TextField("دربارۀ من",blank=True, null=True)
