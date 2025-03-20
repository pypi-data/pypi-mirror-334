# Django Iran SMS

## Overview

A Django-based SMS integration system for simplifying in-country SMS usage in Iran, leveraging the `parsianwebco.ir` service with JWT authentication. Developed by the Chelseru team, this package is designed to support additional services in future releases.

## Features

- Integration with `parsianwebco.ir`
- JWT-based authentication using `rest_framework_simplejwt`
- Scalable and extensible for other SMS providers
- Easy installation and configuration

## Installation

### Prerequisites

- Python 3.11
- Django 5.1 or higher

### Installation via pip

```bash
pip install django-iran-sms
```

### Configuration
In your Django project's settings.py, add the following parameters:

### settings.py

```bash
INSTALLED_APPS = [
...
'drfiransms', # When used in DRF.

]
```

```bash
DJANGO_IRAN_SMS = {
    'AUTHENTICATION': 'rest_framework_simplejwt',  # Specify the authentication method
    'SMS_BACKEND': 'PARSIAN_WEBCO_IR',  # Set the SMS provider backend
    'OTP_CODE': {
        'LENGTH': 8,  # Default length of OTP code = 6
        'EXPIRE_PER_MINUTES': 4,  # Default expiration time per minutes = 2
    },
    'PARSIAN_WEBCO_IR': {
        'API_KEY': 'API_KEY obtained from sms.parsianwebco.ir',  # API key from the SMS provider
        'TEMPLATES': {
            'OTP_CODE': 1,  # Template ID for OTP code
        }
    }
}
```

## Usage
### URL Configuration
In your urls.py, include the following views:

- OTPCodeSend: For sending OTP codes.
- Authentication: For handling authentication and optional registration.
- MessageSend: For sending Messages.

### urls.py
```bash
from drfiransms.views import OTPCodeSend, Authentication, MessageSend

urlpatterns += [
    path('lur/send-code/', OTPCodeSend.as_view(), name='send_code'),  # Endpoint to send OTP code
    path('lur/authentication/', Authentication.as_view(), name='authentication'),  # Endpoint for authentication
    path('lur/send-message/', MessageSend.as_view(), name='send_message'),  # Endpoint to send a message
]
```

## Sending Verification Code via API
To send a POST request for receiving a verification code for a mobile number, use the following structure:

```bash
curl -X POST https://djangoiransms.chelseru.com/lur/send-code/ \
     -H "Content-Type: application/json" \
     -d '{
           "mobile_number": "09123456789"
         }'
```
```bash
curl -X POST https://djangoiransms.chelseru.com/lur/authentication/ \
     -H "Content-Type: application/json" \
     -d '{
           "mobile_number": "09123456789",
           "code": "108117114"
         }'
```
```bash
curl -X POST https://djangoiransms.chelseru.com/lur/send-message/ \
     -H "Content-Type: application/json" \
     -d '{
           "mobile_number": "09123456789",
           "message_text": "hello luristan."
         }'
```
## User Table
This package automatically creates a User table in the Django admin with two fields:

- mobile: Stores the user's mobile number.
- user: A one-to-one relationship with Django's default User model.

## OTP Code Table
This package automatically creates an OTP Code table in the Django admin with two fields:
- mobile: Stores the user's mobile number.
- code: Stores the OTP Code.

## JWT Authentication
This package supports JWT authentication using the rest_framework_simplejwt package. The system is compatible with this authentication method for secure communication with the SMS gateway. Other authentication and login methods are currently under development.

## Future Plans
- Support for additional SMS providers.
- Enhanced error handling.
- Rate limiting and monitoring.
- Contribution

  
Contributions are welcome! Please submit pull requests or report issues on the GitHub repository.

## License
MIT License
