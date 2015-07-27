# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from homepage.forms import ContactModelForm
from django.utils.translation import ugettext_lazy as _

def home(request):
    return render(request, "landing/anasayfa.html")

def what_is_evreka(request):
    return render(request, "landing/nedir.html")

def deger_faydalar(request):
    return render(request, "landing/deger.html")

def how_it_works(request):
    return render(request, "landing/nasil_calisir.html")

def about_us(request):
    return render(request, "landing/hakkimizda.html")

def contact_us(request):
    if request.method == "GET":
        form = ContactModelForm()
        print "get.."
        return render(request, "landing/ulasim.html", {"form" : form})
    else:
        print "post"
        form = ContactModelForm(request.POST)
        if form.is_valid():
            form.save()
            print "ok", form
            return render(request, "landing/ulasim.html", {"form" : form, "success_message" : _("Mesajiniz Gonderildi")})
        else:
            print "not ok", form
            return render(request, "landing/ulasim.html", {"form" : form})