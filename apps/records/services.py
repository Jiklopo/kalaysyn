import numpy as np
from datetime import date
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from apps.records.models import Record, RecordReport


def ceil_division(a, b):
    return -1 * (-a // b)

def filter_empty_data(data, dates):
    new_data = []
    new_dates = []
    for i, v in enumerate(data):
        if not v:
            continue

        new_data.append(v)
        new_dates.append(dates[i])
    
    return (new_data, new_dates)


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


def get_heading_page(title, description=None):
    firstPage = plt.figure()
    firstPage.clf()

    firstPage.text(0.5, 0.65, title, size=24, ha='center')
    firstPage.text(0.5, 0.55, description, size=16, ha='center')
    return firstPage


def get_graph(field_name, data, dates):
    fig, ax = plt.subplots()
    data, dates = filter_empty_data(data, dates)
    fig.autofmt_xdate(rotation=45)
    ax.plot(dates, data)
    ax.set_title(field_name)
    ax.set_xlabel('Date')
    ax.set_ylabel(field_name)
    return fig


def get_pie(title, emotions):
    fig, ax = plt.subplots()
    ax.set_title(title)
    MAX_EMOTIONS = 5
    emotions = np.concatenate(emotions).flat
    unique_emotions, unique_emotions_count = np.unique(        emotions, return_counts=True)
    emotions_count_dict = dict(zip(unique_emotions, unique_emotions_count))
    sorted_emotions = sorted(emotions_count_dict, key=emotions_count_dict.get)[:MAX_EMOTIONS]
    sorted_emotions_count = []
    top_emotions_count = 0
    for e in sorted_emotions:
        cnt = emotions_count_dict.get(e)
        sorted_emotions_count.append(cnt)
        top_emotions_count += cnt

    other_emotions_count = len(emotions) - top_emotions_count
    summary_text = f'Top {MAX_EMOTIONS} emotions amount: {top_emotions_count} ' +\
        f'| Other emotions amount: {other_emotions_count}'
    fig.text(0.5, 0.05, summary_text, ha='center')
    ax.pie(sorted_emotions_count, labels=sorted_emotions, autopct='%1.1f%%')
    ax.axis('equal')
    return fig


def get_table(records, dates):
    cell_labels = ['Date',
                   'Rating',
                   'Sleep Rating',
                   'Fatigue Rating',
                   'Health Rating']
    total_cells = []
    for i, v in enumerate(records):
        total_cells.append([
            dates[i],
            v.rating,
            v.sleep_rating,
            v.fatigue_rating,
            v.health_rating]
        )

    max_rows_on_page = 20  # determined experimentally
    pages_amount = ceil_division(len(total_cells), max_rows_on_page)
    split_cells = np.array_split(total_cells, pages_amount)
    figs = []
    for page in split_cells:
        fig, ax = plt.subplots(1)
        ax.axis('off')
        plt.table(page, colLabels=cell_labels, loc='center', colLoc='center')
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
    emotions = [r.emotions for r in records]

    path = path or f'/tmp/{report.get_file_name()}'
    with PdfPages(path) as pdf:
        pdf.savefig(get_title_page(user, records))
        pdf.savefig(get_heading_page('Rating Graphs',
                    'Separate line graph for each rating type'))
        pdf.savefig(get_graph('Day Rating', ratings, dates))
        pdf.savefig(get_graph('Sleep Rating', sleep_rating, dates))
        pdf.savefig(get_graph('Fatigue Rating', fatigue_rating, dates))
        pdf.savefig(get_graph('Health Rating', health_rating, dates))
        pdf.savefig(get_pie('', emotions))
        pdf.savefig(get_heading_page('Raw data table', 'Table of all records'))
        for fig in get_table(records, dates):
            pdf.savefig(fig)

    return path
