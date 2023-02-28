from django.contrib import admin

from .models import *


#here we difine which tables are going to be shown in admin interface
#we do it by declaring classes for each administrative interface:

# class GeneAttributeLinkInline(admin.TabularInline):
#     model = GeneAttributeLink
#     extra = 3

#configure what to show from each model in admin panel

class PasItemAdmin(admin.ModelAdmin):
    list_display = ('password_id', 'username', 'password', 'url', 'comment', 'pass_category')
    #inlines = [GeneAttributeLinkInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('itemcategory', )


#register each model we wnat to show
admin.site.register(PasItem, PasItemAdmin)
admin.site.register(Category, CategoryAdmin)