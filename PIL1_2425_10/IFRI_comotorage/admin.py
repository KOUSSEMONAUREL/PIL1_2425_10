from django.contrib import admin
from .models import Articles

class AdminArticle(admin.ModelAdmin):
    list_display = ('titre', 'contenue', 'prix', 'image', 'actif')

admin.site.register(Articles, AdminArticle)