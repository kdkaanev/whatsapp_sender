#!/usr/bin/env python
"""
Тестов скрипт за изпращане на WhatsApp съобщение чрез Twilio
"""
import os
import sys
import django
from pathlib import Path

# Добави backend директорията в Python path
sys.path.insert(0, str(Path(__file__).parent))

# Конфигурирай Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from app.services.twilio_service import TwilioService

def send_test_whatsapp():
    """Изпрати тестово WhatsApp съобщение"""
    service = TwilioService()
    
    # Промени номера по желание (трябва да е в формат +1234567890)
    recipient_number = "+359898644178"  # Променя с твой номер
    message_text = "Тестово съобщение от Campaign Manager"
    
    print(f"Изпращане на WhatsApp съобщение до {recipient_number}...")
    result = service.send_whatsapp(recipient_number, message_text)
    
    if result['success']:
        print("✓ Съобщението е изпратено успешно!")
        print(f"Message SID: {result['message_sid']}")
        print(f"Status: {result['status']}")
    else:
        print("✗ Грешка при изпращане на съобщението:")
        print(result['error'])

if __name__ == '__main__':
    send_test_whatsapp()
