import datetime
from datetime import timedelta
from django.views import View
from accounts.permissions import AdminPermissions
from .models import Product, Category
from .serializers import ProductSerializer,QuerySerializer
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated



class ProductGetView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    #get all products which are same slugs
    def get(self, request, slug):
        try:
            selectedproduct = Product.objects.filter(slug=slug)
                          # .filter(Q(expires_at__gte=datetime.datetime.now()-timedelta(days=3)) & Q(expires_at__lte=datetime.datetime.now())))
        except Product.DoesNotExist:
            return Response({'success': False}, status=404)
        selectedproduct_serializer = ProductSerializer(selectedproduct, many=True)
        return Response(selectedproduct_serializer.data)


class ProductPostView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer = ProductSerializer

    # post products
    def post(self, request):
        request.data['user']=request.user.id
        detskiymir_serializer = ProductSerializer(data=request.data)
        detskiymir_serializer.is_valid(raise_exception=True)
        detskiymir_serializer.save()
        return Response(detskiymir_serializer.data)

class ProductUpdate(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    #get only one product

    def put(self, request, pk):
        name = request.POST.get('name')
        price = request.POST.get('price')
        engine = request.POST.get('engine')
        color = request.POST.get('color')




        product_ = Product.objects.get(pk=pk)


        product_.product_type['price']=price
        product_.product_type['name']=name
        if color:
            product_.product_type['color'] = color
        if engine:
            product_.product_type['engine'] = engine
        product_.save()
        product_serializer = ProductSerializer(product_)
        return Response(product_serializer.data)


