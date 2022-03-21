from datetime import datetime
from django.db.models import Q
from rest_framework import filters


class UserFieldFilter(filters.BaseFilterBackend):
    '''
    Filters queryset based on the request user
    '''
    user_field = 'user'
    allow_null = False

    def filter_queryset(self, request, queryset, view):
        user_field = self.extract_value(view, 'user_field', 'get_user_field')
        allow_null = self.extract_value(view, 'allow_null', 'get_allow_null')

        query = Q(**{user_field: request.user})
        if allow_null:
            query = query | Q(**{f'{user_field}__isnull': True})

        return queryset.filter(query)

    def extract_value(self, view, field_name: str, method_name: str):
        method = getattr(view, method_name, None)
        if not method or callable(method):
            return getattr(view, field_name, getattr(self, field_name, None))
        return method()


class DateRangeFilter(filters.BaseFilterBackend):
    date_field = 'date'

    def parse_date(self, request, parameter_name, default) -> datetime:
        date_string = request.query_params.get(parameter_name)
        if not date_string:
            return default

        format = '%d-%m-%y %H:%M'
        try:
            return datetime.strptime(date_string, format)
        except ValueError:
            return default

    def filter_queryset(self, request, queryset, view):
        date_field = getattr(view, 'date_field', self.date_field)
        from_date = self.parse_date(request, 'from', datetime.fromtimestamp(0))
        to_date = self.parse_date(request, 'to', datetime.now())
        return queryset\
            .filter(**{f'{date_field}__gte': from_date, f'{date_field}__lte': to_date})\
            .order_by('date')
