from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.common.filters import UserFieldFilter
from apps.common.mixins import CreateAndAddUserMixin

from apps.common.views import IsAuthenticatedView
from apps.psytests.models import PsyTest, PsyTestRecord
from apps.psytests.serializers import (
    PsyTestDetailsSerializer,
    PsyTestListSerializer,
    PsyTestRatingInputSerializer,
    PsyTestRatingOutputSerializer,
    PsyTestRecordSerializer
)


class PsyTestsListView(IsAuthenticatedView, mixins.ListModelMixin):
    queryset = PsyTest.objects.all()
    serializer_class = PsyTestListSerializer

    def get(self, request):
        return self.list(request)


class PsyTestDetailsView(IsAuthenticatedView, mixins.RetrieveModelMixin):
    serializer_class = PsyTestDetailsSerializer
    queryset = PsyTest.objects.prefetch_related(
        'questions',
        'questions__variants'
    )

    def get(self, request, pk):
        return self.retrieve(request, pk)


class PsyTestRateView(IsAuthenticatedView):
    queryset = PsyTest.objects.all()

    @extend_schema(
        request=PsyTestRatingInputSerializer,
        responses={200: PsyTestRatingOutputSerializer}
    )
    def post(self, request, *args, **kwargs):
        test: PsyTest = self.get_object()
        if test is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        input_serializer = PsyTestRatingInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        rating = input_serializer.validated_data.get('rating')
        test.rate(rating)
        output_serializer = PsyTestRatingOutputSerializer(instance=test)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class RecordListCreateView(IsAuthenticatedView,
                           mixins.ListModelMixin,
                           CreateAndAddUserMixin
                           ):
    queryset = PsyTestRecord.objects.all()
    serializer_class = PsyTestRecordSerializer
    filter_backends = [UserFieldFilter]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class RecordRetrieveUpdateDeleteView(IsAuthenticatedView,
                                     mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin):
    queryset = PsyTestRecord.objects.all()
    serializer_class = PsyTestRecordSerializer
    filter_backends = [UserFieldFilter]

    def get(self, request, pk):
        return self.retrieve(request)
