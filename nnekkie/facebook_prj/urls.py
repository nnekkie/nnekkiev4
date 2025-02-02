
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.flatpages import views
from core.routing import websocket_urlpatterns
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.conf.urls import *
from core.sitemaps import *
from error import views
sitemaps = {
    # 'static': StaticSitemap,
    'flatpages':FlatPageSitemap,
    'posts': PostSitemap,
    
}

urlpatterns = [
    # for product api
    path('', include('pwa.urls')),
    path("", include("core.urls")),
    path('error/',include("error.urls")),
    path(r'query/', include('haystack.urls')),
    path('product/', include('product.urls')),
    path('product/api/v1/', include('djoser.urls')),
    # Fundraiser
    path('product/api/v1/', include('djoser.urls.authtoken')),
    path('grc/', include('grc.urls')),
    path('purchases/', include('purchases.urls')),
    path('forum/', include('forum.urls')),
    path('blog/', include('blog.urls')),
    path('robot.txt/', TemplateView.as_view(template_name='robot.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap',),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('admin_tools_stats/', include('admin_tools_stats.urls')), 
    path('__debug__/', include('debug_toolbar.urls')),

    path('accounts/', include('allauth.urls')),
    # Routing
    path("user/", include("userauths.urls")),
    path('event/', include('event.urls')),
    

    path("fund/", include("fundraiser.urls")),


    # admin doc 
    

    # page, event, video
    path("addon/", include("addon.urls")),

    # Web Socket
    path('ws/', include(websocket_urlpatterns)),

    # Change Password
    path('user/change-password/',auth_views.PasswordChangeView.as_view(template_name='userauths/password-reset/change-password.html',success_url = '/user/password-reset-complete/'),name='change_password'),
    path('user/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='userauths/password-reset/password_reset_complete.html'), name='password_reset_complete'),

    # flatpages url
    path('flatpages/', include('django.contrib.flatpages.urls')),
    path('comments/', include('django_comments.urls')),
    
    

]

handler400 = "error.views.handler400"
handler403 = "error.views.handler403"
handler404 = "error.views.handler404"
handler500 = "error.views.handler500"
# urlpatterns += [
#     path('about-us/', views.flatpage, {"url":'/about-us/'}, name='about'),
#     path('contact-us/', views.flatpage, {'url':'/contact-us'}, name='contact'),
#     path('t-c/', views.flatpage, {'url':'/t-c/'}, name='t-c'),
#     path()
# ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

