from django.contrib import admin
from evrekaTest.models import Bin,BinSensorRecord,RouteDetailRecord,Route,Vehicle,RequestErrorLog,ForecastingRecord,ClientRecord,ForecastingResult#,NavigationRecord

# Register your models here.
class CustomModelAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


@admin.register(Bin)
class BinAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

@admin.register(ForecastingRecord)
class ForecastingRecordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

@admin.register(ForecastingResult)
class ForecastingResultAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

#@admin.register(BinVisitHistory)
#class BinVisitHistoryAdmin(CustomModelAdminMixin, admin.ModelAdmin):
#    pass

@admin.register(ClientRecord)
class ClientRecordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

#@admin.register(NavigationRecord)
#class NavigationRecordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
#    pass

@admin.register(BinSensorRecord)
class BinSensorRecordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

@admin.register(RouteDetailRecord)
class BinVisitRecordAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('route','bin', 'show_route_date')

    def show_route_date(self,model):
        return model.route.date
    show_route_date.admin_order_field = 'route__date'

@admin.register(Route)
class RouteAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

@admin.register(Vehicle)
class VehicleAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(RequestErrorLog)
class RequestErrorLogAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    list_display = ('level','message','date',)
    list_filter = ('level',)
    search_fields = ('level','message',)

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('level','message','date')


