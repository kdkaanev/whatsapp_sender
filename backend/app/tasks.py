from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from app.models import Message, Campain
from authentication.models import CampainUser
from app.services.twilio_service import TwilioService
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_campaign_sms_task(campaign_id, message_body):
    """
    Asynchronous task to send SMS to all contacts in a campaign
    """
    try:
        campaign = Campain.objects.get(id=campaign_id)
        twilio_service = TwilioService()
        results = twilio_service.send_campaign_sms(campaign, message_body)
        
        logger.info(f"Campaign SMS sent. Successful: {len(results['successful'])}, Failed: {len(results['failed'])}")
        
        return {
            'status': 'completed',
            'successful': len(results['successful']),
            'failed': len(results['failed']),
            'campaign_id': campaign_id
        }
    except Exception as e:
        logger.error(f"Error sending campaign SMS: {str(e)}")
        raise


@shared_task
def send_campaign_whatsapp_task(campaign_id, message_body):
    """
    Asynchronous task to send WhatsApp to all contacts in a campaign
    """
    try:

        campaign = Campain.objects.get(id=campaign_id)
        campaign.status = 'sending'
        campaign.save(update_fields=['status'])
        twilio_service = TwilioService()
        results = twilio_service.send_campaign_whatsapp(campaign, message_body)

        campaign.status = 'sent'
        campaign.save(update_fields=['status'])
        
        logger.info(f"Campaign WhatsApp sent. Successful: {len(results['successful'])}, Failed: {len(results['failed'])}")

        return {
            'status': 'completed',
            'successful': len(results['successful']),
            'failed': len(results['failed']),
            'campaign_id': campaign_id
        }
    except Exception as e:
        logger.error(f"Error sending campaign WhatsApp: {str(e)}")
        raise


@shared_task
def send_single_sms_task(phone_number, message_body):
    """
    Asynchronous task to send single SMS
    """
    try:
        twilio_service = TwilioService()
        result = twilio_service.send_sms(phone_number, message_body)
        
        logger.info(f"Single SMS sent to {phone_number}")
        return result
    except Exception as e:
        logger.error(f"Error sending single SMS: {str(e)}")
        raise


@shared_task
def send_single_whatsapp_task(phone_number, message_body):
    """
    Asynchronous task to send single WhatsApp
    """
    try:
        twilio_service = TwilioService()
        result = twilio_service.send_whatsapp(phone_number, message_body)
        
        logger.info(f"Single WhatsApp sent to {phone_number}")
        return result
    except Exception as e:
        logger.error(f"Error sending single WhatsApp: {str(e)}")
        raise

@shared_task
def send_activation_email(user_id):
    
        user = CampainUser.objects.get(id=user_id)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        activation_link = (
        f"https://campaingnflow.com/api/auth/activate/{uid}/{token}/"
    )
        context = {
            'user': user,
            'activation_link': activation_link,
        }
        
        html_content = render_to_string('emails/activate_account.html', context)
        email = EmailMultiAlternatives(
            subject="Activate your CampaignFlow account",
            body=(
                f"Please activate your account by clicking this link: "
                f"{activation_link}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)