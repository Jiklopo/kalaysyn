import os
from pathlib import Path
from datetime import date
from django.core.management.base import BaseCommand
from apps.authentication.models import User

from apps.records import ReportStatusChoices
from apps.records.models import Record, RecordReport
from apps.records.services import generate_report_file

class Command(BaseCommand):
    help = 'Generate Test PDF'


    def handle(self, *args, **kwargs):
        user = User.objects.first()
        report: RecordReport = RecordReport(
            user=user,
            from_date=date.fromtimestamp(0),
            to_date=date.today()
        )
        report_path = generate_report_file(report, 'test.pdf')
