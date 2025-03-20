import requests, json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ParsianWebcoIr:
    """
        token
        TemplateID
        MessageVars
        Receiver
        delay
    """
    TOKEN = None
    HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
    def __init__(self, mobile, *args, **kwargs):
        try:
            # Give TOKEN from DJANGO_IRAN_SMS { PARSIAN_WEBCO_IR { TOKEN } }
            if not hasattr(settings, 'DJANGO_IRAN_SMS'):
                raise ImproperlyConfigured('DJANGO_IRAN_SMS must be defined in settings.py .')

            if 'PARSIAN_WEBCO_IR' not in settings.DJANGO_IRAN_SMS:
                raise ImproperlyConfigured('PARSIAN_WEBCO_IR must be defined in settings.py -> DJANGO_IRAN_SMS.')

            if 'API_KEY' not in settings.DJANGO_IRAN_SMS['PARSIAN_WEBCO_IR']:
                raise ImproperlyConfigured('API_KEY must be defined in settings.py -> DJANGO_IRAN_SMS:PARSIAN_WEBCO_IR.')
        except ImproperlyConfigured as e:
            print(f"Configuration Error: {e}")
            raise
        else:
            self.TOKEN = settings.DJANGO_IRAN_SMS['PARSIAN_WEBCO_IR']['API_KEY']
        self.RECEIVER = mobile

    def send_otp_code(self, code, template_id=None):
        try:
            if not template_id:
                if not hasattr(settings, 'DJANGO_IRAN_SMS'):
                    raise ImproperlyConfigured('DJANGO_IRAN_SMS must be defined in settings.py .')

                if 'PARSIAN_WEBCO_IR' not in settings.DJANGO_IRAN_SMS:
                    raise ImproperlyConfigured('PARSIAN_WEBCO_IR must be defined in settings.py -> DJANGO_IRAN_SMS.')

                if 'TEMPLATES' not in settings.DJANGO_IRAN_SMS['PARSIAN_WEBCO_IR']:
                    raise ImproperlyConfigured('TEMPLATES must be defined in settings.py -> DJANGO_IRAN_SMS:PARSIAN_WEBCO_IR.')

                if 'OTP_CODE' not in settings.DJANGO_IRAN_SMS['PARSIAN_WEBCO_IR']['TEMPLATES']:
                    raise ImproperlyConfigured('OTP_CODE must be defined in settings.py -> DJANGO_IRAN_SMS:PARSIAN_WEBCO_IR:TEMPLATES.')

                template_id = settings.DJANGO_IRAN_SMS['PARSIAN_WEBCO_IR']['TEMPLATES']['OTP_CODE']

            api_url = 'https://api.parsianwebco.ir/webservice-send-sms/send'
            data = {
                'token': self.TOKEN,
                'TemplateID': template_id,
                'MessageVars': code,
                'Receiver': self.RECEIVER,
                'delay': 1
            }
            return json.loads(requests.post(url=api_url, data=data, headers=self.HEADERS).content)
            """
                response:
                    status:
                        200 ok
                        100 faild
                        401 no authenticated
            """
        except ImproperlyConfigured as e:
            print(f"Configuration Error: {e}")
            raise
        return False

    def send_message(self, message, template_id):
        try:
            api_url = 'https://api.parsianwebco.ir/webservice-send-sms/send'
            data = {
                'token': self.TOKEN,
                'TemplateID': template_id,
                'MessageVars': message,
                'Receiver': self.RECEIVER,
                'delay': 1
            }
            return json.loads(requests.post(url=api_url, data=data, headers=self.HEADERS).content)
            """
                response:
                    status:
                        200 ok
                        100 faild
                        401 no authenticated
            """
        except:
            return False
