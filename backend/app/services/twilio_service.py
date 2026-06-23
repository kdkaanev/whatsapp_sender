from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from app.models import Message
import logging

logger = logging.getLogger(__name__)


class TwilioService:
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        self.whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, to_phone_number, message_body):
        """
        Send SMS message via Twilio
        """
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.phone_number,
                to=to_phone_number
            )
            logger.info(f"SMS sent successfully. SID: {message.sid}")
            return {
                'success': True,
                'message_sid': message.sid,
                'status': message.status
            }
        except TwilioRestException as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def send_whatsapp(self, to_phone_number, message_body):
        """
        Send WhatsApp message via Twilio
        """
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.whatsapp_number,
                to=f"whatsapp:{to_phone_number}"
            )
            logger.info(f"WhatsApp sent successfully. SID: {message.sid}")
            return {
                'success': True,
                'message_sid': message.sid,
                'status': message.status
            }
        except TwilioRestException as e:
            logger.error(f"Error sending WhatsApp: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def send_campaign_sms(self, campaign, message_template):
        """
        Send SMS to all contacts in a campaign
        """
        contacts = campaign.contact_set.all()
        results = {
            'successful': [],
            'failed': []
        }

        for contact in contacts:
            result = self.send_sms(contact.phone_number, message_template)
            
            if result['success']:
                Message.objects.create(
                    campain=campaign,
                    contact=contact,
                    status='sent',
                    send_at=None
                )
                results['successful'].append({
                    'contact': contact.name,
                    'phone': contact.phone_number,
                    'sid': result['message_sid']
                })
            else:
                Message.objects.create(
                    campain=campaign,
                    contact=contact,
                    status='failed'
                )
                results['failed'].append({
                    'contact': contact.name,
                    'phone': contact.phone_number,
                    'error': result['error']
                })

        return results

    def send_campaign_whatsapp(self, campaign, message_template):
        """
        Send WhatsApp to all contacts in a campaign
        """
        contacts = campaign.contact_set.all()
        results = {
            'successful': [],
            'failed': []
        }

        for contact in contacts:
            result = self.send_whatsapp(contact.phone_number, message_template)
            
            if result['success']:
                Message.objects.create(
                    campain=campaign,
                    contact=contact,
                    status='sent',
                    send_at=None
                )
                results['successful'].append({
                    'contact': contact.name,
                    'phone': contact.phone_number,
                    'sid': result['message_sid']
                })
            else:
                Message.objects.create(
                    campain=campaign,
                    contact=contact,
                    status='failed'
                )
                results['failed'].append({
                    'contact': contact.name,
                    'phone': contact.phone_number,
                    'error': result['error']
                })

        return results
