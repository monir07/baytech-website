from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your models here.
class Notice(models.Model):
    ref_no = models.CharField(max_length=250, blank=True, null=True)
    publish_date = models.DateTimeField()
    subject = models.CharField(max_length=250)
    body = HTMLField()
    
    initial_by = models.CharField(max_length=50)
    initial_designation = models.CharField(max_length=100)
    initial_sign = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')   


    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = ('-id',)


class Noc(models.Model):
    publish_date = models.DateTimeField()
    description = models.TextField()
    attachment = models.FileField(upload_to='nocAttachment/')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')   


    def __str__(self):
        return str(self.description)

    class Meta:
        ordering = ('-id',)