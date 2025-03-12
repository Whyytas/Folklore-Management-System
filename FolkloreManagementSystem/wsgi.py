import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FolkloreManagementSystem.settings")

try:
    application = get_wsgi_application()
except Exception as e:
    error_msg = traceback.format_exc()
    sys.stderr.write(error_msg + "\n")  # Print error to logs
    raise
