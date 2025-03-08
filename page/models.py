from django.db import models
from django.contrib.auth import get_user_model
from base.helpers.validators import file_size_validator
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class ProjectTypeChoices(models.TextChoices):
    NEW = 'new_building', 'New Building'
    REPAIR = 'repair', 'Repair'

class ProjectCategoryChoices(models.TextChoices):
    ONGOING = 'on_going', 'On Going'
    COMPLETED = 'completed', 'Completed'

class JobTypeChoices(models.TextChoices):
    FULL = 'full_time', 'Full Time'
    PART = 'part_time', 'Part Time'


# PROJECT PAGES START FROM HERE
class Project(models.Model):
    proejct_no = models.CharField(max_length=15, unique=True)
    proejct_name = models.CharField(max_length=150)
    proejct_type = models.CharField(max_length=25, choices=ProjectTypeChoices.choices)  # new-building
    proejct_category = models.CharField(max_length=25, choices=ProjectCategoryChoices.choices)  # on-going
    length = models.CharField(max_length=25)
    breadth = models.CharField(max_length=25)
    depth = models.CharField(max_length=25)
    draft = models.CharField(max_length=25)
    max_speed = models.CharField(max_length=25)
    special_feature = models.TextField()
    project_photo = models.ImageField(upload_to='project/', validators=[file_size_validator], help_text="File size should be less than 3mb(.doc/.pdf)")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')   

    def __str__(self):
        return f"{self.proejct_no}:{self.proejct_name}"


class ProjectInformation(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    contract_date = models.DateField()
    delivery_date = models.DateField()
    classification = models.CharField(max_length=25)
    client = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')

    def __str__(self):
        return f"{self.project.proejct_no}:{self.project.proejct_name}"


class ProjectMachinery(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    main_engine = models.CharField(max_length=150)
    engine_power = models.CharField(max_length=80)
    engine_quantity = models.IntegerField()
    main_dg = models.CharField(max_length=150)
    dg_power = models.CharField(max_length=80)
    dg_quantity = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')   

    def __str__(self):
        return f"{self.project.proejct_no}:{self.project.proejct_name}"



# NEWS AND INSIGHT PAGES START FROM HERE
class NewsInsight(models.Model):
    head_line = models.CharField(max_length=150)
    publish_date = models.DateField()
    body = models.TextField()
    cover_photo = models.ImageField(upload_to='news/', validators=[file_size_validator], help_text="File size should be less than 3mb(.doc/.pdf)")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')   



# NEWS AND INSIGHT PAGES START FROM HERE
class TeamMember(models.Model):
    name = models.CharField(max_length=80)
    designation = models.CharField(max_length=60)
    short_description = models.TextField()
    photo = models.ImageField(upload_to='teams/', validators=[file_size_validator], help_text="File size should be less than 3mb(.doc/.pdf)")
    phone_no = models.CharField(max_length=20)
    email_address = models.EmailField(max_length=25)
    facebook = models.URLField()
    twitter = models.URLField()
    instagram = models.URLField()
    linkedin = models.URLField()
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')  


# JOB POST PAGES START FROM HERE
class Responsibility(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class EducationalRequirement(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class ExperienceRequirement(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class AdditionalRequirement(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Benifit(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    published_date = models.DateField()
    deadline = models.DateField()
    job_type = models.CharField(max_length=25, choices=JobTypeChoices.choices)
    vacancy = models.IntegerField()
    salary = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()

    job_responsibilities = models.ManyToManyField(Responsibility, blank=True)
    educational_requirements = models.ManyToManyField(EducationalRequirement, blank=True)
    experience_requirements = models.ManyToManyField(ExperienceRequirement, blank=True)
    additional_requirements = models.ManyToManyField(AdditionalRequirement, blank=True)
    benifits = models.ManyToManyField(Benifit, blank=True)

    location = models.TextField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')  

    def __str__(self):
        return self.title
    
# CONTACT US PAGES START FROM HERE
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    contact_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}: {self.contact_no}"