from celery import shared_task
from app.models import Message, Campain
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
