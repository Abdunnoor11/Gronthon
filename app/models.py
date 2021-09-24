from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import os

# Create your models here.
class Files(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    pdf = models.FileField(upload_to='pdf')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.pdf.name)

class Image(models.Model):
    pdf = models.ForeignKey(Files, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='pics')

    def __str__(self):
        return os.path.basename(self.image.name)

class Text(models.Model):
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    text = RichTextField(blank=True, null=True)


