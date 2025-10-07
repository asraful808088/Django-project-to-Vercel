import os
from django.core.wsgi import get_wsgi_application

# Set your Django settings module (replace `bank` if your project folder name is different)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')

# Create the WSGI application object for Vercel
app = get_wsgi_application()
