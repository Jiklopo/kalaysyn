from django.core.files.base import ContentFile
from apps.records.services import generate_report_file

from configuration.celery import app
from apps.records import ReportStatusChoices
from apps.records.models import RecordReport


@app.task(bind=True)
def generate_report_task(self, report_id):
    try:
        report: RecordReport = RecordReport.objects.get(id=report_id)
    except RecordReport.DoesNotExist:
        return

    report.status = ReportStatusChoices.PROCESSING.value
    report.save()
    report_path = generate_report_file(report)
    if not report_path:
        report.status = ReportStatusChoices.ERROR.value
        report.save()
        return

    report.status = ReportStatusChoices.READY.value
    with open(report_path, 'rb') as f:
        report.file.save(report.get_file_name(), ContentFile((f.read())))

    report.save()
