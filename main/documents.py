from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product


@registry.register_document
class DocumentProduct(Document):
    class Index:
        name = 'main'
        search = {'number_of_shards': 1, 'number_of_replicas': 0}

        # Assuming your JSON field is named 'json_field'
        # title = fields.TextField(attr='product_type.title')
        # slug = fields.TextField(attr='slug')
        # description = fields.TextField(attr='product_type.description')
        # price = fields.FloatField(attr='product_type.price')
        # color = fields.TextField(attr='product_type.color')

    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    slug = fields.TextField(
        attr='slug',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })

    color = fields.TextField(
        attr='color',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })



    class Django:
        model = Product