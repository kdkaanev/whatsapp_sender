from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import Contact, Campain, Message, Template, WebhookEvent
from .serializers import ContactSerializer, CampainSerializer, MessageSerializer, TemplateSerializer, WebhookEventSerializer
from .services.twilio_service import TwilioService


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Contact created successfully',
            'contact': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


class ContactListView(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contact.objects.filter(user=self.request.user).order_by('-created_at')
        search = self.request.query_params.get('search')
        tag = self.request.query_params.get('tag')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(phone_number__icontains=search)
            )
        if tag:
            queryset = queryset.filter(tags__contains=[tag])
        return queryset


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Contact updated successfully',
            'contact': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        contact_name = instance.name
        self.perform_destroy(instance)
        return Response({
            'message': f'Contact "{contact_name}" deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


# Campaign Views
class CampainCreateView(generics.CreateAPIView):
    serializer_class = CampainSerializer
    permission_classes = [IsAuthenticated]
    queryset = Campain.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Campaign created successfully',
            'campaign': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


class CampainListView(generics.ListAPIView):
    serializer_class = CampainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campain.objects.filter(user=self.request.user)


class CampainDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CampainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campain.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Campaign updated successfully',
            'campaign': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        campaign_name = instance.name
        self.perform_destroy(instance)
        return Response({
            'message': f'Campaign "{campaign_name}" deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class TemplateCreateView(generics.CreateAPIView):
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Template.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Template created successfully',
            'template': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


class TemplateListView(generics.ListAPIView):
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Template.objects.filter(user=self.request.user).order_by('-id')


class TemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Template.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Template updated successfully',
            'template': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        template_name = instance.name
        self.perform_destroy(instance)
        return Response({
            'message': f'Template "{template_name}" deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


# Message Views
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        campaign_id = self.request.query_params.get('campaign_id')
        status_filter = self.request.query_params.get('status')
        
        queryset = Message.objects.filter(campain__user=self.request.user)
        
        if campaign_id:
            queryset = queryset.filter(campain_id=campaign_id)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset


class MessageStatisticsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campaign_id = request.query_params.get('campaign_id')
        
        try:
            campaign = Campain.objects.get(id=campaign_id, user=request.user)
        except Campain.DoesNotExist:
            return Response(
                {'error': 'Campaign not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        messages = Message.objects.filter(campain=campaign)
        
        stats = {
            'total': messages.count(),
            'sent': messages.filter(status='sent').count(),
            'delivered': messages.filter(status='delivered').count(),
            'failed': messages.filter(status='failed').count(),
            'scheduled': messages.filter(status='scheduled').count(),
        }
        
        stats['success_rate'] = round(
            (stats['delivered'] / stats['total'] * 100) if stats['total'] > 0 else 0, 2
        )

        return Response({
            'campaign': CampainSerializer(campaign).data,
            'statistics': stats
        }, status=status.HTTP_200_OK)


class DashboardStatisticsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_contacts = Contact.objects.filter(user=user).count()

        campaigns = Campain.objects.filter(user=user)
        total_campaigns = campaigns.count()
        active_campaigns = campaigns.filter(status='active').count()

        messages = Message.objects.filter(campain__user=user)
        delivered_count = messages.filter(status='delivered').count()
        sent_count = messages.filter(status__in=['sent', 'delivered']).count()
        attempted_count = messages.filter(status__in=['sent', 'delivered', 'failed']).count()

        delivery_rate = round((delivered_count / attempted_count * 100), 2) if attempted_count > 0 else 0

        return Response({
            'total_contacts': total_contacts,
            'campaigns': {
                'total': total_campaigns,
                'active': active_campaigns,
            },
            'messages_sent': sent_count,
            'delivery_rate': delivery_rate,
        }, status=status.HTTP_200_OK)


class MessageByCampaignView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        campaign_id = self.kwargs.get('campaign_id')
        return Message.objects.filter(
            campain_id=campaign_id,
            campain__user=self.request.user
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        try:
            campaign = Campain.objects.get(id=kwargs['campaign_id'], user=request.user)
        except Campain.DoesNotExist:
            return Response(
                {'error': 'Campaign not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        stats = {
            'total': queryset.count(),
            'sent': queryset.filter(status='sent').count(),
            'delivered': queryset.filter(status='delivered').count(),
            'failed': queryset.filter(status='failed').count(),
            'scheduled': queryset.filter(status='scheduled').count(),
        }

        return Response({
            'campaign': CampainSerializer(campaign).data,
            'statistics': stats,
            'messages': serializer.data
        }, status=status.HTTP_200_OK)


# SMS/WhatsApp Views
class SendSMSView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):
        try:
            campaign = Campain.objects.get(id=campaign_id, user=request.user)
        except Campain.DoesNotExist:
            return Response(
                {'error': 'Campaign not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        message_body = request.data.get('message')
        if not message_body:
            return Response(
                {'error': 'Message body is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from app.tasks import send_campaign_sms_task
        task = send_campaign_sms_task.delay(campaign_id, message_body)

        return Response({
            'message': 'SMS campaign is being sent',
            'task_id': task.id,
            'campaign_id': campaign_id
        }, status=status.HTTP_202_ACCEPTED)


class SendWhatsAppView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):
        try:
            campaign = Campain.objects.get(id=campaign_id, user=request.user)
        except Campain.DoesNotExist:
            return Response(
                {'error': 'Campaign not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        message_body = request.data.get('message')
        if not message_body:
            return Response(
                {'error': 'Message body is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from app.tasks import send_campaign_whatsapp_task
        task = send_campaign_whatsapp_task.delay(campaign_id, message_body)

        return Response({
            'message': 'WhatsApp campaign is being sent',
            'task_id': task.id,
            'campaign_id': campaign_id
        }, status=status.HTTP_202_ACCEPTED)


class TaskStatusView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        from celery.result import AsyncResult
        
        task = AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'current': 0,
                'total': 100,
                'status': 'Task is waiting for execution'
            }
        elif task.state == 'PROGRESS':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 100),
                'status': task.info.get('status', '')
            }
        elif task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'current': 100,
                'total': 100,
                'status': 'Task executed successfully',
                'result': task.result
            }
        elif task.state == 'FAILURE':
            response = {
                'state': task.state,
                'current': 0,
                'total': 100,
                'status': str(task.info),
                'error': str(task.traceback)
            }
        else:
            response = {
                'state': task.state,
                'current': 0,
                'total': 100,
                'status': 'Task status unknown'
            }
        
        return Response(response, status=status.HTTP_200_OK)
