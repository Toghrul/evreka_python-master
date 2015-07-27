from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from evreka import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^routing/', include('evrekaTest.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^site/', include('homepage.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'homepage.views.home'),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)