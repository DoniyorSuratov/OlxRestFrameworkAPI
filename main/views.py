from .custom_filters import ProductFilter
from .documents import DocumentProduct
from .models import Product, Category, Favourite
from .serializers import ProductSerializer, FavouritsSerializer, ProductDocumentSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from elasticsearch_dsl import Search, Q
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, FilteringFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_filters import rest_framework as filters
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)


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






class ProductDeleteView(GenericAPIView):
    serializer = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        # Ensure the product exists and is owned by the current user
        try:
            product = Product.objects.get(pk=pk, user=request.user)
            product.delete()
            return Response({"detail": "Product delated"})
        except Product.DoesNotExist:
            return Response({"detail": "Product not found or you don't have permission to delete it."},
                            status=status.HTTP_404_NOT_FOUND)




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


class ProductGetVip(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.filter(status=3)
        product_serializer = ProductSerializer(products, many=True)
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

class ProductSearchViewSet(DocumentViewSet):
    document = DocumentProduct
    serializer_class = ProductDocumentSerializer
    pagination_class = CustomPageNumberView

    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'slug',
        'title',
        'color',
    )

    filter_fields = {
        'title': 'title',
        'slug': 'slug',
        'color': 'color',
    }

    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'slug': {
            'field': 'slug.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'color': {
            'field': 'color.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        }
    }
    def list(self, request, *args, **kwargs):
        search_term = self.request.query_params.get('search', '')

        # Check if the search term is empty or too short
        # if len(search_term) == 0:
        # Handle short or empty search term (adjust the condition as needed)
        # return Response([])

        # Use a Q object to build a more robust query
        query = Q('multi_match', query=search_term, fields=self.search_fields)

        # Apply the query to the queryset
        queryset = self.filter_queryset(self.get_queryset().query(query))
        print('Queryset >>>>>', queryset)

        # Perform pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductFilterView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = ()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
