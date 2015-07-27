# coding=utf-8
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

class ContactModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"İsim"))
    email = models.EmailField(verbose_name=_(u"E-Posta"))
    message = models.TextField(verbose_name=_(u"Mesajınız"))