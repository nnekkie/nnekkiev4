from django import forms
from .models import *
from django.forms import modelformset_factory, inlineformset_factory

input_css_class = 'form-control'


class ProductAttachForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = ProductAttachment
        fields = ['book','name', 'is_free']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['is_free']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class



class ProductForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Product
        fields = ['image','name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class ProductUpdateForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Product
        fields = ['image','name', 'handle', 'price']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


ProductAttachmentModelFormset = modelformset_factory(
    ProductAttachment,
    form=ProductAttachForm,
    fields = ['book', 'name', 'is_free'],
    extra=0,
    can_delete=True
)

ProductAttachmentInlineModelFormset = inlineformset_factory(
    Product,
    ProductAttachment,
    form=ProductAttachForm,
    formset=ProductAttachmentModelFormset,
    fields = ['book', 'name', 'is_free'],
    extra=0,
    can_delete=True
)

