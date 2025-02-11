"""
WSGI config for OOD project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from waitress import serve
from whitenoise import WhiteNoise

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OOD.settings')

# Import the Django application
application = get_wsgi_application()

# Add WhiteNoise middleware to serve static files
application = WhiteNoise(application, root=settings.STATIC_ROOT)

# Start the Waitress server
serve(application, host='localhost', port=8000,threads=2)