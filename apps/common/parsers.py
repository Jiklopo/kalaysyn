from rest_framework.parsers import FileUploadParser


class NoFileNameFileUploadParser(FileUploadParser):
    def get_filename(self, stream, media_type, parser_context):
        filename, extension = media_type.split('/')
        return f'{filename}.{extension}'