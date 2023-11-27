from .models import Product, Category, Favourite
from .serializers import ProductSerializer, FavouritsSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


# class ProductGetView(GenericAPIView):#get all products which are same slugs
#     permission_classes = ()
#     serializer_class = ProductSerializer
#
#     def get(self, request, slug):
#         try:
#             selectedproduct = Product.objects.filter(slug=slug)
#                           # .filter(Q(expires_at__gte=datetime.datetime.now()-timedelta(days=3)) & Q(expires_at__lte=datetime.datetime.now())))
#         except Product.DoesNotExist:
#             return Response({'success': False}, status=404)
#         selectedproduct_serializer = ProductSerializer(selectedproduct, many=True)
#         return Response(selectedproduct_serializer.data)



class ProductGetView(GenericAPIView):#get all products
    permission_classes = ()
    serializer_class = ProductSerializer

    def get(self, request):
        try:
            selectedproduct = Product.objects.all()
        except Product.DoesNotExist:
            return Response({'success': False}, status=404)
        selectedproduct_serializer = ProductSerializer(selectedproduct, many=True)
        return Response(selectedproduct_serializer.data)



class UserAdverView(GenericAPIView):    #Get all advertisement of authenticated user
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get(self, request):
        product = Product.objects.filter(user=request.user)
        print(product)
        product_serializer = ProductSerializer(product, many=True)
        return Response(product_serializer.data)



class ProductPostView(GenericAPIView): #Posting advertisement
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductSerializer


    def post(self, request):
        request.data['user']=request.user.id
        product_serializer = ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)


class ProductDeleteView(GenericAPIView): #Delete own advertisement
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer = ProductSerializer
    def delete(self, request, pk):
        Product.objects.get(Q(pk=pk) & Q(user=request.user)).delete()
        product = Product.objects.all()
        product_serializer = ProductSerializer(product, many=True)
        return Response(product_serializer.data)


class ProductUpdate(GenericAPIView):    #Changing own advertisement infos
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        name = request.data.get('name')
        price = request.data.get('price')
        engine = request.data.get('engine')
        color = request.data.get('color')
        room_num =request.data.get('room_num')
        square = request.data.get('square')
        distance =request.data.get('distance')
        stage =request.data.get('stage')
        status =request.data.get('status')

        product_ = Product.objects.get(Q(user=request.user) & Q(pk=pk)) #gets only this users advertisements

        #changes product_type infos
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



class FavouriteAdverView(GenericAPIView):
    queryset = Favourite.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouritsSerializer

    def post(self, request, pk):
        user = request.user
        product = Product.objects.get( pk=pk)

        favourits = Favourite.objects.create(
            user=user,
            product=product
        )
        favourits_serializer = FavouritsSerializer(favourits)
        return Response(favourits_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            favourite = Favourite.objects.get(pk=pk, user=request.user)
            favourite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favourite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FavouriteGetView(GenericAPIView): #getting favourite items
    queryset = Favourite.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouritsSerializer

    def get(self, request):
        try:
            my_favourites = Favourite.objects.filter(user=request.user)
        except Favourite.DoesNotExist:
            return Response({'succes': "You don't have favourite items "},status=404 )

        favourite_serializer = FavouritsSerializer(my_favourites, many=True)
        return Response(favourite_serializer.data)



class CustomPageNumberView(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100