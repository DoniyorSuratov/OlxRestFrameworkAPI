import datetime
from datetime import timedelta
from django.views import View
from accounts.permissions import AdminPermissions
from .models import CreateAdvertisementDetskiymir
from .serializers import AdvertisementDetskiymirSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class GetAdvertisementDetskiymirView(GenericAPIView):
    permission_classes = ()
    serializer_class = AdvertisementDetskiymirSerializer

    def get(self, request, slug):
        # detskiymir = CreateAdvertisementDetskiymir.objects.all()
        try:
            detskiymir = CreateAdvertisementDetskiymir.objects.get(slug=slug)
                          # .filter(Q(expires_at__gte=datetime.datetime.now()-timedelta(days=3)) & Q(expires_at__lte=datetime.datetime.now())))
        except CreateAdvertisementDetskiymir.DoesNotExist:
            return Response({'success': False}, status=404)
        detskiymir_serializer = AdvertisementDetskiymirSerializer(detskiymir)
        return Response(detskiymir_serializer.data)

class CreateAdvertisementDetskiymirView(GenericAPIView):
    permission_classes = (AdminPermissions, )
    serializer = AdvertisementDetskiymirSerializer

    def post(self, request):
        detskiymir_serializer = AdvertisementDetskiymirSerializer(data=request.data)
        detskiymir_serializer.is_valid(raise_exception=True)
        detskiymir_serializer.save()
        return Response(detskiymir_serializer.data)
