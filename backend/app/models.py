from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"
    
class Campain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE, related_name='messages')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    send_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message_sid = models.CharField(max_length=255, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message for {self.campain.name} at {self.send_at}"
    
class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.name
    
class WebhookEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    event = models.CharField(max_length=50)

    def __str__(self):
        return f"Webhook for {self.event} to {self.url}"
