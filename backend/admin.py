from django.contrib import admin

from backend.models import Shop

# admin.site.register(Shop)

@admin.register(Shop)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','url']

