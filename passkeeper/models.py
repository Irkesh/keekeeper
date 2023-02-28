from django.db import models

# Create your models here.


class Category(models.Model):
    itemcategory = models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return self.itemcategory


class PasItem(models.Model):    
    password_id = models.CharField(max_length=256, null=False, blank=False)
    username = models.CharField(max_length=256, null=False, blank=False)
    password = models.CharField(max_length=256, null=False, blank=False)
    url = models.CharField(max_length=256, null=False, blank=True)
    #own = models.CharField(max_length=2, default="Me")
    comment = models.CharField(max_length=256, null=False, blank=True)
    pass_category = models.ForeignKey(Category, on_delete=models.CASCADE )
    
    def __str__(self):
        return self.password_id