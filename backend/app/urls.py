from django.urls import path
from .views import (
    ContactCreateView, ContactListView, ContactDetailView,
    CampainCreateView, CampainListView, CampainDetailView,
    TemplateCreateView, TemplateListView, TemplateDetailView,
    SendSMSView, SendWhatsAppView, TaskStatusView,
    MessageListView, MessageStatisticsView, MessageByCampaignView
)
from .import_views import ContactImportView

urlpatterns = [
    # Contact endpoints
    path('contacts/', ContactListView.as_view(), name='contact-list'),
    path('contacts/create/', ContactCreateView.as_view(), name='contact-create'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('contacts/import/', ContactImportView.as_view(), name='contact-import'),
    
    # Campaign endpoints
    path('campaigns/', CampainListView.as_view(), name='campaign-list'),
    path('campaigns/create/', CampainCreateView.as_view(), name='campaign-create'),
    path('campaigns/<int:pk>/', CampainDetailView.as_view(), name='campaign-detail'),

    # Template endpoints
    path('templates/', TemplateListView.as_view(), name='template-list'),
    path('templates/create/', TemplateCreateView.as_view(), name='template-create'),
    path('templates/<int:pk>/', TemplateDetailView.as_view(), name='template-detail'),

    # Send campaign messages (async)
    path('campaigns/<int:campaign_id>/send-sms/', SendSMSView.as_view(), name='send-sms'),
    path('campaigns/<int:campaign_id>/send-whatsapp/', SendWhatsAppView.as_view(), name='send-whatsapp'),
    
    # Task status
    path('tasks/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
    
    # Message history and statistics
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('campaigns/<int:campaign_id>/messages/', MessageByCampaignView.as_view(), name='campaign-messages'),
    path('campaigns/<int:campaign_id>/statistics/', MessageStatisticsView.as_view(), name='campaign-statistics'),
]
