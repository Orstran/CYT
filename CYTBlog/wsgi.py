import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CYTBlog.settings')  # 修复这里

application = get_wsgi_application()