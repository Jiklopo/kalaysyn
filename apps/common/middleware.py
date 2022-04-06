from os import getenv
import sys
import traceback
from django.http import JsonResponse
from configuration.settings import DEBUG
from sentry_sdk import capture_exception


class JsonExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.is_sentry_enabled = not bool(getenv('DISABLE_SENTRY'))

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not DEBUG:
            raise exception
        
        type, message, tb = sys.exc_info()
        data = {
            'type': str(type),
            'message': str(message),
            'traceback': traceback.format_exception(type, message, tb)
        }
        if self.is_sentry_enabled:
            capture_exception(exception)
        return JsonResponse(data=data, safe=False, status=500)
