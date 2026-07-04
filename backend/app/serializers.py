from rest_framework import serializers
from .models import Contact, Campain, Message, Template, WebhookEvent


class ContactSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='phone_number')
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone', 'tags', 'created_at', 'user')
        read_only_fields = ('id', 'user', 'created_at')


class CampainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campain
        fields = ('id', 'name', 'description', 'user', 'status', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'campain', 'contact', 'status', 'send_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'name', 'content', 'user')
        read_only_fields = ('id', 'user')


class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = ('id', 'url', 'event', 'user')
        read_only_fields = ('id', 'user')
