from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from django.db import models

class University(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    abr = models.CharField(max_length=8, blank=False, null=False)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.abr + " | " + self.name

class Section(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=False, null=False)
    def __str__(self):
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=False, null=False)
    university = models.ForeignKey(University, verbose_name=("دانشگاه"), on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Education(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=False, null=False)
    def __str__(self):
        return self.name + " | " + self.slug

class ScientificGrade(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=False, null=False)
    level = models.CharField(blank=False, null=False, choices=[("1", "1"), ("2","2"), ("3","3")])
    def __str__(self):
        return self.name


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
    def get_name(self):
        if self.en_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.fn_fa} {self.ln_fa}"

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
    
    def has_fa_name(self):
        if self.fn_fa and self.ln_fa:
            if len(self.fn_fa+self.ln_fa) > 5:
                return True
            else: return False
        else: return False
    
    def has_profile(self):
        try:
            profile = self.student_profile
            if profile:
                return True
        except:
            return False
    
    def is_professor(self):
        try:
            profile = self.professor_profile
            if profile:
                return True
        except:
            return False
        
    def __str__(self):
        try:
            profile = self.professor_profile
            if profile:
                return f"دکتر {self.fn_fa} {self.ln_fa} | {profile.section}"
        except:
            return self.username
        
class StudentProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='student_profile')
    verified = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    working_university = models.ForeignKey(University, null=True, on_delete=models.SET_NULL)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    semester_of_entrance = models.PositiveSmallIntegerField(blank=True, null=True)
    student_id = models.CharField(max_length=12, blank=True, null=True, unique=True)
    date_added = models.DateField(auto_now_add=True)
    verified_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_name()} (دانشجو)"
    
    class Meta:
        verbose_name = "پروفایل دانشجو"
        verbose_name_plural = "پروفایل دانشجویان"

class ProfessorProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='professor_profile')
    working_university = models.ForeignKey(University, null=True, on_delete=models.PROTECT)
    year_of_recruitment = models.PositiveSmallIntegerField(blank=True, null=True)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.PROTECT)
    location = models.ManyToManyField(Location)
    education = models.ForeignKey(Education, null=True, blank=True, on_delete=models.PROTECT)
    grade = models.ForeignKey(ScientificGrade, null=True, blank=True, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    academic_email = models.EmailField(blank=True, null=True, unique=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_name()} | (استاد)"
    
    class Meta:
        verbose_name = "پروفایل استاد"
        verbose_name_plural = "پروفایل استادان"