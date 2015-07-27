from django.contrib import admin
from homepage.models import ContactModel


class CustomModelAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


@admin.register(ContactModel)
class ContactModelAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

