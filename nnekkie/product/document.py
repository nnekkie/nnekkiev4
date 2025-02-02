from django_elasticsearch_dsl import Document

from django_elasticsearch_dsl.registries import registry

from .models import *

class ProductDocument(Document):
    class Index:
        name = 'Product'
        settings = {'numbers_of_shard':1, 'number_of_replicas':0}

    class Django :
        model = ProductAttachment
        fields  = {'name', 'book', 'product'}