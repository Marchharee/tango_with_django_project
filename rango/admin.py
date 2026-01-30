from django.contrib import admin

# Register your models here.
from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display=('title','category','url')
class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
