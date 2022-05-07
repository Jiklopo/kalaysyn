#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def try_initialize_debugger():
    if not os.getenv('DEBUGGER'):
        return

    import debugpy
    try:
        debugpy.listen(('0.0.0.0', 3000))
    except:
        return
    print('Waiting for vs code debugger...')
    debugpy.wait_for_client()
    print('Debugger attached!')


def main():
    try_initialize_debugger()
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
