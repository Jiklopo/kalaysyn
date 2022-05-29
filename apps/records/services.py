from datetime import date
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from apps.records.models import Record, RecordReport


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


def get_graph(field_name, data, dates):
    fig, ax = plt.subplots()
    fig.autofmt_xdate(rotation=45)
    ax.plot(dates, data)
    ax.set_title(field_name)
    ax.set_xlabel('Date')
    ax.set_ylabel(field_name)
    return fig


def get_table(field_name, data, dates):
    cell_labels = ['Date',
                   'Rating',
                   'Sleep Rating',
                   'Fatigue Rating',
                   'Health Rating']
    total_cells = []
    for i, v in enumerate(data):
        total_cells.append([
            dates[i],
            v.rating,
            v.sleep_rating,
            v.fatigue_rating,
            v.health_rating]
        )

    max_rows_on_page = 20 # determined experimentally
    pages_amount = len(total_cells) // max_rows_on_page
    split_cells = np.array_split(total_cells, pages_amount)
    figs = []
    for page in split_cells:
        fig, ax = plt.subplots(1)
        ax.axis('off')
        table = plt.table(page, colLabels=cell_labels, loc='center',colLoc='center')
        figs.append(fig)
    return figs


def generate_report_file(report: RecordReport, path=None):
    user = report.user
    records = list(Record.objects
                   .order_by('date')
                   .filter(
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

    path = path or f'/tmp/{report.get_file_name()}'
    with PdfPages(path) as pdf:
        pdf.savefig(get_title_page(user, records))
        pdf.savefig(get_graph('Day Rating', ratings, dates))
        pdf.savefig(get_graph('Sleep Rating', sleep_rating, dates))
        pdf.savefig(get_graph('Fatigue Rating', fatigue_rating, dates))
        pdf.savefig(get_graph('Health Rating', health_rating, dates))
        for fig in get_table('Table', records, dates):
            pdf.savefig(fig)

    return path
