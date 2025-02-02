from haystack import indexes
from .models import *

class ProductIndex(indexes.BasicSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # name = indexes.CharField(model_attr='name')
    # price = indexes.DecimalField(model_attr='price')
    # handle = indexes.CharField(model_attr='handle')
    handle = indexes.EdgeNgramField(model_attr='handle')
    name = indexes.CharField(model_attr='name', faceted=True)
    price = indexes.DecimalField(model_attr='price', faceted=True)
    description = indexes.EdgeNgramField(model_attr='description')
    image = indexes.CharField(model_attr='image', null=True)

    def get_model(self):
        return Product
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image.url else ''
    # def product_attachment(self, obj):
    #     return [
    #         f"{attachment.book.url} : {attachment.name}"
    #         for attachment in obj.productattachment_set.all()
    #     ]

    # def product(self, obj):
    #     data = super().prepare(obj)
    #     data['attachments'] = self.product_attachment(obj)
    #     return data


class ProductAttachmentIndex(indexes.BasicSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', faceted=True,)
    file = indexes.CharField(model_attr='book')
    description = indexes.CharField(model_attr='description')
    is_free = indexes.BooleanField(model_attr='is_free', faceted=True)

    def get_model(self):
        return ProductAttachment
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    
    def get_file_url(self, obj):
        return obj.file.url if obj.file.url else ''

