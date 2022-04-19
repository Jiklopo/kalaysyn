import matplotlib.pyplot as plt
from datetime import date
from django.core.management.base import BaseCommand
from matplotlib.backends.backend_pdf import PdfPages

from apps.authentication.models import User
from apps.records.models import Record


class Command(BaseCommand):
    help = 'Generate Test PDF'

    def get_title_page(self, user, records):
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

    def get_plot(self, field_name, data, dates):
        fig, ax = plt.subplots()
        ax.plot(dates, data)
        ax.set_title(field_name)
        ax.set_xlabel('Date')
        ax.set_ylabel(field_name)
        return fig

    def handle(self, *args, **options):
        user = User.objects.first()
        records = list(Record.objects.filter(user=user))

        dates = [r.date for r in records]
        ratings = [r.rating for r in records]
        sleep_rating = [r.sleep_rating for r in records]
        fatigue_rating = [r.fatigue_rating for r in records]
        health_rating = [r.health_rating for r in records]

        with PdfPages('test.pdf') as pdf:
            pdf.savefig(self.get_title_page(user, records))
            pdf.savefig(self.get_plot('Day Rating', ratings, dates))
            pdf.savefig(self.get_plot('Sleep Rating', sleep_rating, dates))
            pdf.savefig(self.get_plot('Fatigue Rating', fatigue_rating, dates))
            pdf.savefig(self.get_plot('Health Rating', health_rating, dates))
