from django.db.models import Q
from rest_framework import filters


class UserFieldFilter(filters.BaseFilterBackend):
    user_field = 'user'
    allow_null = False

    def filter_queryset(self, request, queryset, view):
        user_field = getattr(view, 'user_field', self.user_field)
        allow_null = getattr(view, 'allow_null', self.allow_null)

        query = Q(**{user_field: request.user})
        if allow_null:
            query = query | Q(**{f'{user_field}__isnull': True})
        
        return queryset.filter(query)


