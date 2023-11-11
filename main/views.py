import datetime
from datetime import timedelta
from django.views import View
from accounts.permissions import AdminPermissions
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated



class ProductGetView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    def get(self, request, slug):
        # detskiymir = CreateAdvertisementDetskiymir.objects.all()
        try:
            selectedproduct = Product.objects.get(slug=slug)
                          # .filter(Q(expires_at__gte=datetime.datetime.now()-timedelta(days=3)) & Q(expires_at__lte=datetime.datetime.now())))
        except Product.DoesNotExist:
            return Response({'success': False}, status=404)
        selectedproduct_serializer = ProductSerializer(selectedproduct)
        return Response(selectedproduct_serializer.data)

class ProductPostView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer = ProductSerializer

    def post(self, request):
        request.data['user']=request.user.id
        detskiymir_serializer = ProductSerializer(data=request.data)
        detskiymir_serializer.is_valid(raise_exception=True)
        detskiymir_serializer.save()
        return Response(detskiymir_serializer.data)
