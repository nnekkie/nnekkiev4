from django.shortcuts import render

# Create your views here.


def handler404(request, exception=None):
    return render(request, 'error/handler404.html', status=404)

def handler403(request, exception=None):
    return render(request, 'error/handler403.html', status=403)

def handler400(request, exception):
    return render(request, 'error/handler400.html', status=400)
def handler500(request):
    return render(request, 'error/handler500.html', status=500)