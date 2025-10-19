# +++++++++++ DJANGO WSGI CONFIGURATION FOR PYTHONANYWHERE +++++++++++
# 
# This file contains the WSGI configuration required to serve up your
# Django application on PythonAnywhere.
#
# INSTRUCTIONS:
# 1. Go to your PythonAnywhere Web tab
# 2. Click on the WSGI configuration file link
# 3. Replace the entire contents with this file's contents
# 4. Update the paths below if your project location is different
# 5. Make sure you've set up your virtualenv in the Web tab
# 6. Click "Reload" button to apply changes
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import sys

# Add your project directory to the sys.path
# IMPORTANT: Update this path to match your actual project location on PythonAnywhere
path = '/home/UjaanRakshit/ujaan-moviesstore'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
# This tells Django where to find your settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesstore.settings'

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
