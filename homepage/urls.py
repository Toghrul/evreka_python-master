from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'home/$', 'homepage.views.home', name="evreka_anasayfa"),
                       url(r'nedir/$', 'homepage.views.what_is_evreka' , name="evreka_nedir"),
                       url(r'deger/$', 'homepage.views.deger_faydalar' , name="evreka_deger"),
                       url(r'nasil/$', 'homepage.views.how_it_works', name="evreka_nasil"),
                       url(r'hakkimizda/$', 'homepage.views.about_us', name="evreka_hakkimizda"),
                       url(r'bize_ulasin/$', 'homepage.views.contact_us', name="evreka_ulasim"),
                       url(r'$', 'homepage.views.home', name="evreka_anasayfa"),

)
