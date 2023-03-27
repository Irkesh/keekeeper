from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
# Create your models here.



class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    organisation = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    salt = models.BinaryField(null=True, blank=True)
    

    def __unicode__(self):
        return self.user.username

class Category(models.Model):
    itemcategory = models.CharField(max_length=256, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.itemcategory


class PasItem(models.Model):    
    password_id = models.CharField(max_length=256, null=False, blank=False)  #title - how user decide to call it
    username = models.CharField(max_length=256, null=False, blank=False)     #username to store
    password = models.CharField(max_length=256, null=False, blank=False)     #password to store
    url = models.CharField(max_length=256, null=False, blank=True)
    #own = models.CharField(max_length=2, default="Me")
    comment = models.CharField(max_length=256, null=False, blank=True)
    pass_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.password_id



class PasItemTemplate(models.Model):    
    password_id_temp = models.CharField(max_length=256, null=False, blank=False)  #title - how user decide to call it
    username_temp = models.CharField(max_length=256, null=False, blank=False)     #username to store
    password_temp = models.CharField(max_length=256, null=False, blank=False)     #password to store
    url_temp = models.CharField(max_length=256, null=False, blank=True)
    #own = models.CharField(max_length=2, default="Me")
    comment_temp = models.CharField(max_length=256, null=False, blank=True)
    
    def __str__(self):
        return self.password_id


class CategoryTemplate(models.Model):
    itemcategory_temp = models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return self.itemcategory_temp