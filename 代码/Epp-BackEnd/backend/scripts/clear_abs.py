import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from business.models import AbstractReport

def refresh():
    for report in AbstractReport.objects.all():
        if not os.path.exists(report.report_path) or not report.report_path.endswith('.pdf'):
            report.delete()
            
if __name__ == '__main__':
    refresh()