import datetime
from datetime import timedelta
from django.views import View
from accounts.permissions import AdminPermissions
from .models import Product, Category
from .serializers import ProductSerializer
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


#Get all advertisement of authenticated user
class UserAdverView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get(self, request):
        product = Product.objects.filter(user=request.user)
        print(product)
        product_serializer = ProductSerializer(product, many=True)
        return Response(product_serializer.data)


#Posting advertisement
class ProductPostView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer = ProductSerializer


    def post(self, request):
        request.data['user']=request.user.id
        detskiymir_serializer = ProductSerializer(data=request.data)
        detskiymir_serializer.is_valid(raise_exception=True)
        detskiymir_serializer.save()
        return Response(detskiymir_serializer.data)


#Changing advertisement infos
class ProductUpdate(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        print(request.data)
        name = request.data.get('name')
        price = request.data.get('price')
        engine = request.data.get('engine')
        color = request.data.get('color')
        room_num =request.data.get('room_num')
        square = request.data.get('square')
        distance =request.data.get('distance')
        stage =request.data.get('stage')
        status =request.data.get('status')

        product_ = Product.objects.get(Q(user=request.user) & Q(pk=pk))

        print(product_.product_type)
        product_.product_type.update({'price' : price})
        product_.product_type.update({'name' : name})
        if color:
            product_.product_type.update({'color' : color})
        if engine:
            product_.product_type.update({'engine' : engine})
        if room_num:
            product_.product_type.update({'room_num' : room_num})
        if square:
            product_.product_type.update({'square' : square})
        if distance:
            product_.product_type.update({'distance' : distance})
        if stage:
            product_.product_type.update({'stage' : stage})
        if status:
            product_.product_type.update({'status' : status})

        product_.save()
        product_serializer = ProductSerializer(product_)
        return Response(product_serializer.data)


