from .models import *
from django.db import models 
from haystack import signals
from haystack.query import SearchQuerySet

class ProductOnlySignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        models.signals.post_save.connect(self.handle_save, sender=Product)
        models.signals.post_delete.connect(self.handle_delete, sender=Product)


    def teardown(self):
        models.signals.post_save.disconnect(self.handle_save, sender=Product)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Product)

    def handle_save(self, sender, instance, **kwargs):
        print(f"saved product :{instance}")
        
        SearchQuerySet().update_object(instance)

        if kwargs.get('created', False):
            instance.index()
    

    def handle_delete(self, sender, instance, **kwargs):
        print(f"deleted product :{instance} ")

        SearchQuerySet.remove_object(instance)

class ProductAttachmentSignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        models.signals.post_save.disconnect(self.handle_save, sender=ProductAttachment)
        models.signals.post_delete.disconnect(self.handle_delete, sender=ProductAttachment)

    def teardown(self):
        models.signals.post_save.disconnect(self.handle_save, sender=ProductAttachment)
        models.signals.post_delete.disconnect(self.handle_delete, sender=ProductAttachment)

    def handle_save(self, sender, instance, **kwargs):
        print(f"saved product :{instance}")
        
        SearchQuerySet().update_object(instance)

        if kwargs.get('created', False):
            instance.index()
    

    def handle_delete(self, sender, instance, **kwargs):
        print(f"deleted product :{instance} ")

        SearchQuerySet.remove_object(instance)