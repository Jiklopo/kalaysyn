from datetime import date
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from django.core.files.base import ContentFile

from configuration.celery import app
from apps.records import ReportStatusChoices
from apps.records.models import Record, RecordReport


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


def get_title_page(user, records):
    firstPage = plt.figure()
    firstPage.clf()
    title = f'Summary for {user.get_full_name()}'
    period = f'{records[0].date} - {records[-1].date}'
    given_date = f'Created: {date.today()}'
    disclamer = 'This report MUST NOT be used for self-diagnosis.\n' +\
        'Please, visit a professional if you need any help.'

    firstPage.text(0.5, 0.75, title, size=24, ha='center')
    firstPage.text(0.5, 0.65, period, size=16, ha='center')
    firstPage.text(0.5, 0.60, given_date, size=10, ha='center')
    firstPage.text(0.5, 0.05, disclamer, size=10, ha='center')
    return firstPage


def get_plot(field_name, data, dates):
    fig, ax = plt.subplots()
    ax.plot(dates, data)
    ax.set_title(field_name)
    ax.set_xlabel('Date')
    ax.set_ylabel(field_name)
    return fig


def generate_report_file(report: RecordReport):
    user = report.user
    records = list(Record.objects.filter(
        user=user,
        date__gte=report.from_date,
        date__lte=report.to_date
    ))
    if len(records) == 0:
        return None

    dates = [r.date for r in records]
    ratings = [r.rating for r in records]
    sleep_rating = [r.sleep_rating for r in records]
    fatigue_rating = [r.fatigue_rating for r in records]
    health_rating = [r.health_rating for r in records]

    path = f'/tmp/{report.get_file_name()}'
    with PdfPages(path) as pdf:
        pdf.savefig(get_title_page(user, records))
        pdf.savefig(get_plot('Day Rating', ratings, dates))
        pdf.savefig(get_plot('Sleep Rating', sleep_rating, dates))
        pdf.savefig(get_plot('Fatigue Rating', fatigue_rating, dates))
        pdf.savefig(get_plot('Health Rating', health_rating, dates))

    return path
