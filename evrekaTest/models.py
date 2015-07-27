# -*- coding: utf-8 -*-
from datetime import datetime as dt
from django.db import models
from time import mktime
from django.forms import ModelForm

class ClientRecord(models.Model):
    client_id = models.AutoField(verbose_name="Client ID", primary_key=True)
    client_name = models.CharField(max_length=30, default="-")
    info = models.TextField(blank=True, null=True, verbose_name="Info")
    jsonfile = models.FileField(verbose_name="JSON File",blank=True,null=True)
    duration_matrix_txt = models.FileField(verbose_name="Duration Matrix TXT",blank=True,null=True)
    distance_matrix_txt = models.FileField(verbose_name="Distance Matrix TXT",blank=True,null=True)

    def __str__(self):
        return (self.client_name).encode(encoding='utf-8')

class Bin(models.Model):
    bin_id = models.IntegerField(primary_key=True, verbose_name="Bin ID")
    sensor_id = models.CharField(max_length=200, default="X")
    latitude = models.FloatField(verbose_name="Lat.")
    longitude = models.FloatField(verbose_name="Long.")
    info = models.TextField(blank=True, null=True, verbose_name="Info")

    size = models.FloatField(default=1,verbose_name="Size of Bin")
    client = models.ForeignKey(ClientRecord)
    measurement_freq = models.IntegerField(verbose_name="Measurement (times per connection)",default=8) # baglandiginda kac olcum veriyor
    connection_freq = models.IntegerField(verbose_name="Connection Frequency (in minutes) ",default=480) # kac dakikada bir baglaniyor

    def __str__(self):
        return str(self.bin_id)

    def latest_record(self):
        today = dt.now()
        records = BinSensorRecord.objects.filter(bin=self, date__startswith=today.date()).order_by('-date')
        if len(records) > 0:
            return records[0]
        else:
            records = BinSensorRecord.objects.filter(bin=self, date__lte=today.date()).order_by('-date')
            if len(records) > 0:
                return records[0]
            return None

    current_record = property(latest_record)



class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, verbose_name="Vehicle ID")
    fuel_consumption = models.FloatField(verbose_name="Fuel Consumption per 100 km (in litres)", default=10)
    plate = models.CharField(verbose_name="Plate", max_length=10, default="")

    number_of_trip = models.IntegerField(default=1)
    capacity = models.FloatField(verbose_name="Vehicle Capacity to store waste in meter cube",default=0)
    work_time = models.FloatField(verbose_name="Time to work per day in minutes",default=0)
    use_for_routing = models.BooleanField(default=False)
    client = models.ForeignKey(ClientRecord)

    def __str__(self):
        return self.plate

class BinSensorRecord(models.Model):
    SensRecord_id = models.AutoField(primary_key=True, verbose_name="Sensor Record ID")
    bin = models.ForeignKey(Bin)
    fullness_rate = models.FloatField(verbose_name="Fullness Rate")
    battery_rate = models.FloatField(verbose_name="Battery Rate")
    temperature = models.FloatField(verbose_name="Temperature")
    date = models.DateTimeField(default=dt.now, blank=True, verbose_name="Record Date")
    is_working = models.BooleanField(default=True, verbose_name="Sensors Working")

    def _get_date_epoch(self):
        return int(mktime(self.date.timetuple()) * 1000)

    date_as_timestamp = property(_get_date_epoch)


class Route(models.Model):
    route_id = models.AutoField(primary_key=True, verbose_name="Route ID")
    processed_kml_file = models.FileField(verbose_name="Route KML file (generated)", blank=True, null=True)
    real_kml_file = models.FileField(verbose_name="Route KML file (GPS data)", blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, blank=True, null=True)
    duration = models.FloatField(verbose_name="Duration", blank=True, default=0.0)
    total_km = models.FloatField(verbose_name="Total KM", blank=True, default=0.0)
    date = models.DateTimeField(default=dt.now, blank=True, verbose_name="Date")

    assign_date = models.DateTimeField(null=True, blank=True, verbose_name="Assignment Date")
#    source = models.CharField(max_length=30, verbose_name="Source of Route", default="Optimization Algorithm")

    def co2_emission(self):
        if self.vehicle:
            return self.vehicle.fuel_consumption * 26.5 * self.total_km
        else:
            return 0

    def __unicode__(self):
        return self.vehicle.plate + " - " + str(self.date)


class RouteUploadForm(ModelForm):
    class Meta:
        model = Route
        fields = ('processed_kml_file', )


class RouteDetailRecord(models.Model):
    detail_id = models.AutoField(primary_key=True, verbose_name="Route Detail ID")
    bin = models.ForeignKey(Bin)
    route = models.ForeignKey(Route)
    unique_together = ("bin", "route")

    def route_date(self):
        return self.route.date

#class BinVisitHistory(models.Model):
#    hist_id = models.AutoField(primary_key=True, verbose_name="Visit History ID")
#    bin = models.ForeignKey(Bin)
#    date = models.DateTimeField(default=dt.now, blank=True, verbose_name="Date")
#    is_visited = models.BooleanField(default=False, verbose_name="Bin Visited")
#    unique_together = ("bin", "date")

#    def __str__(self):
#        return str(self.hist_id)

#class NavigationRecord(models.Model):
#    vehicle = models.ForeignKey(Vehicle)
#    route = models.ForeignKey(Route)

#    def route_assign_date(self):
#        return self.route.assign_date

class ForecastingRecord(models.Model):
    forecast_id = models.AutoField(verbose_name="Forecasting ID", primary_key=True)
    bin = models.ForeignKey(Bin)
    date = models.DateTimeField(verbose_name="Date", default=dt.now)
    is_visited = models.BooleanField(verbose_name="Visit Status on Field", default=False)
    last_fullness_rate = models.FloatField(verbose_name="Fullness Rate Before Routing")

"""
 Forecastingresults  farklı objeleri tutacağı için Forecastinrecord dan ayrıldı. Fieldler aynı.
 Results : predicted values,
 Records : real values.
"""

class ForecastingResult(models.Model):
    result_id = models.AutoField(verbose_name="Prediction ID", primary_key=True)
    bin = models.ForeignKey(Bin)
    date = models.DateTimeField(verbose_name="Prediction Date", default=dt.now)
    is_visit_predicted = models.BooleanField(verbose_name="Visit Status on Prediction", default=True)
    last_fullness_rate_predicted = models.FloatField(verbose_name="Predicted Rate for Future")

# class RequestLog(models.Model):
# date = models.DateTimeField(default=datetime.now, blank=True, verbose_name="LogDate")
#    type = models.CharField(verbose_name="Method", max_length=20, default="")
#    client_ip = models.CharField(verbose_name="Client IP", max_length=20, default="")
#    result = models.CharField(verbose_name="Result", max_length=20, default="Unknown")

#    def __str__(self):
#        return self.result

class RequestErrorLog(models.Model):
    level = models.CharField(max_length=30)
    message = models.TextField()
    date = models.DateTimeField('date', null=True, blank=True)
