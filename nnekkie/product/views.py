# In your views.py
from django.shortcuts import render, redirect, get_object_or_404, Http404
from .forms import *
from .models import *
from django.http import *
import mimetypes
from facebook_prj.storages.utils import generat_presigned_url
from purchases.models import *
from django.urls import reverse
from django.db.models  import Q
from haystack.query import SearchQuerySet



# def search_view(request):
#     query = request.GET.get('q', '').strip()  # Strip extra spaces
#     results = []  # Default to an empty list
    
#     if query:  # Proceed only if query is not empty
#         try:
#             sqs = SearchQuerySet().autocomplete(content_auto=query)
#             results = sqs[:10]  # Limit the results to 10 items
#         except Exception as e:
#             # Log the exception and gracefully handle it
#             print(f"Error during search: {e}")
#             results = []

#     return render(request, 'search/result.html', {
#         'query': query,
#         'results': results,
#     })




def purchased(request, book_id):
    purchases = Purchase.objects.filter(user=request.user, is_free=True)
    return render(request, 'core/index.html', {'resource':purchases})


def search_product(request):
    query = request.GET.get('p')  # Get the search query parameter
    search_data = []
    
    if query:  # If there's a query, perform the search
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(handle__icontains=query)
        ).distinct()  # Use `distinct` to avoid duplicates

        for product in products:
            # Try to get the first related attachment, or provide a default fallback
            attachment = ProductAttachment.objects.filter(product=product).first()
            attachment_file = attachment.book.url if attachment and attachment.book else None
            attachment_name = attachment.name if attachment else "No attachment"
            is_free = attachment.is_free if attachment else False

            # Add product data to the response
            search_data.append({
                'name': product.name,
                'attachment_file': attachment_file,
                'attachment_name': attachment_name,
                'is_free': is_free,
            })

    # Return the JSON response
    return JsonResponse({'products': search_data})


def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachment = ProductAttachment.objects.filter(product=obj)
    # attachment = obj.productattachment_set.all()
    is_owner = False
    if request.user.is_authenticated:
        # request.session['']
        is_owner = request.user.purchase_set.all().filter(product=obj, completed=True).exists()
    context = {'product':obj, 'is_owner':is_owner, "attachment":attachment}

    return render(request, 'product/detail.html', context)

def product_attachment_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated and can_download is False:
        can_download = request.user.purchase_set.all().filter(product=attachment.product, completed=True).exists()
    if can_download  is False:
        return HttpResponseBadRequest()
    file_name = attachment.book.name
    file_url = generat_presigned_url(file_name)
    # filename = attachment.book.name
    # content_type, _ = mimetypes.guess_type(filename)
    # response =  FileResponse(file)
    # response['Content-Type'] =content_type or 'application/octet-stream'
    # response['Content-Disposition'] = f"attachment;filename={filename}"

    return HttpResponseRedirect(file_url)



def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachment = ProductAttachment.objects.filter(product=obj)

    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {'product':obj}
    if not is_manager:
        return HttpResponseBadRequest()
    
    form = ProductUpdateForm(request.POST or None,request.FILES or None, instance=obj)
    formset = ProductAttachmentInlineModelFormset(request.POST or None, request.FILES or None ,queryset=attachment)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            attachment_obj = _form.save(commit=False)
            is_delete = _form.cleaned_data.get("DELETE")

            if is_delete:
                if attachment_obj.pk:
                    attachment_obj.delete()
            else:
                attachment_obj.product = instance
                attachment_obj.save()
        # return redirect('product/create/')
        return redirect(reverse('product:manage', kwargs={'handle':obj.handle}))
    context['form'] = form
    context['formset'] = formset
    return render(request, 'product/manager.html', context)

def product_list_view(request):
    objects_list = Product.objects.all()
    context= {
        'product_list': objects_list
    }
    return  render(request, 'product/list.html', context)

def create_product_view(request):
    context = {}

    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()

            return redirect(obj.get_manage_url())
        else:
            form.add_error('You must be logged in')
    context['form'] = form
    return render(request, 'product/create.html', context)