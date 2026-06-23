from rest_framework import serializers
from .models import Contact, Campain, Message, Template, WebhookEvent


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone_number', 'user')
        read_only_fields = ('id', 'user')


class CampainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campain
        fields = ('id', 'name', 'description', 'user')
        read_only_fields = ('id', 'user')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'campain', 'contact', 'status', 'send_at')
        read_only_fields = ('id',)


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
