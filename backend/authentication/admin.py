from django.contrib import admin

from .models import CampainUser

# Register your models here.



admin.site.register(CampainUser)
class CampainUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
