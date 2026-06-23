from django.contrib import admin

from .models import Campain, Contact, Message

# Register your models here.
admin.site.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'phone_number')
    ordering = ('name',)

admin.site.register(Campain)
class CampainAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'description')
    ordering = ('name',)

admin.site.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('campain', 'contact', 'status', 'send_at')
    list_filter = ('status', 'send_at')
    search_fields = ('campain__name', 'contact__name')
    ordering = ('send_at',)