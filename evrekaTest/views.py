# coding=utf-8
import json
from datetime import datetime, timedelta
import time
import random
from django.db.models import Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from evrekaTest.models import Vehicle, Route, Bin, RouteDetailRecord, BinSensorRecord, RouteUploadForm, ForecastingRecord, ForecastingResult
from django.core import serializers
import dateutil.parser
import logging
import numpy as np
from django.contrib.auth.decorators import user_passes_test
from django.http import QueryDict

postlogger = logging.getLogger('inputlogs')


def kml_test(request):

    return render(request, "kml_test.html")
def selam(request):
    bin = Bin.objects.all()
    vehicle = Vehicle.objects.all()
    return render(request, "selam.html", {'bins': bin, 'vehicles': vehicle})
def yeni(request):
    bin = Bin.objects.all()
    vehicle = Vehicle.objects.all()
    return render(request, "yeni.html", {'bins': bin, 'vehicles': vehicle})
def vehiclepost(request):
    print "heee"
    return HttpResponse("Success")

def kml_test_mapbox(request):
    return render(request, "map_box.html")


def dashboard_home(request):
    #TODO burdali visits kaldirilmali. index.html e dinamik veri cekme getirilmeli
    #Django-rest-framework belki?
    #Index.html deki tarih secme bozuluyor. Sabah-oglen-aksam rotalari birbirine karisacak
    vehicle = Vehicle.objects.all()
    visits = [{"raw": x['date'].isoformat(), "local": x['date'].date()} for x in
              Route.objects.order_by('-date').values('date').distinct()]
    return render(request, "dashboard/index.html", {'vehicles': vehicle, 'visits': visits})


def dashboard_vehicles(request):
    #TODO burdali visits kaldirilmali. index.html e dinamik veri cekme getirilmeli
    #Django-rest-framework belki?
    #Index.html deki tarih secme bozuluyor. Sabah-oglen-aksam rotalari birbirine karisacak
    vehicle = Vehicle.objects.all()
    visits = [{"raw": x['date'].isoformat(), "local": x['date'].date()} for x in
              Route.objects.order_by('-date').values('date').distinct()]
    return render(request, "dashboard/vehicles.html", {'vehicles': vehicle, 'visits': visits})


def dashboard_bins(request):
    bin = Bin.objects.all()
    # print Bin.objects.all().annotate(Avg('latest_record__fullness_rate'))
    return render(request, "dashboard/bins.html", {'bins': bin})


# AJAX VIEWS
def get_kml(request):
    if request.method == "GET":
        print request.GET
        the_date = dateutil.parser.parse(request.GET.get("isodate"))
        vehicle = Vehicle.objects.get(pk=request.GET.get("vehicle_pk"))
        #FIXME Buraya dikkat. The_date.date() bu kaldirilmali! tam net tarih girilmeli ve o cekilmeli
        #Integer timestamp kullanilmali! startswith kaldirilmali.
        candidate_routes = Route.objects.filter(date__startswith=the_date.date(), vehicle=vehicle).order_by('-date')
        if len(candidate_routes) > 0:
            message = {"state": "success", "processed_kml": candidate_routes[0].processed_kml_file.url}
            return HttpResponse(json.dumps(message), content_type="application/json")
        else:
            message = {"state": "fail", "message": "Bu arac ve tarih icin bir rota bulunmuyor.."}
            return HttpResponse(json.dumps(message), content_type="application/json")
    message = {"state": "fail", "message": "Bu adrese POST request atilamaz!"}
    return HttpResponse(json.dumps(message), content_type="application/json")


def get_last_7_day_all(request):
    if request.method == "GET":
        result = []
        date_ago = datetime.now() - timedelta(days=7)
        while date_ago <= datetime.now():
            candidates = Route.objects.filter(date__startswith=date_ago.date())
            if len(candidates) > 0:
                visited_count = sum([RouteDetailRecord.objects.filter(route=rt).count() for rt in candidates])
                result.append({"date": date_ago.date().isoformat(),
                               "value": candidates.aggregate(Sum('total_km'))['total_km__sum'],
                               "bin_count": visited_count})
            date_ago += timedelta(days=1)
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return HttpResponse("You cannot POST here.")


def get_last_7_day_bin_fullness(request):
    if request.method == "GET":
        result = []
        date_ago = datetime.now() - timedelta(days=7)
        while date_ago <= datetime.now():
            candidates = BinSensorRecord.objects.filter(date__startswith=date_ago.date())
            if len(candidates) > 0:
                result.append({"date": date_ago.date().isoformat(),
                               "value": candidates.aggregate(Avg('fullness_rate'))['fullness_rate__avg'] * 100})
            date_ago += timedelta(days=1)
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return HttpResponse("You cannot POST here.")


def get_last_7_day_specific_vehicle(request, vehicle_pk=None):
    if request.method == "GET" and vehicle_pk:
        result = []
        date_ago = datetime.now() - timedelta(days=7)
        print Vehicle.objects.all().values('pk')
        while date_ago <= datetime.now():
            candidates = Route.objects.filter(date__startswith=date_ago.date(), vehicle__pk=vehicle_pk)
            print candidates
            if len(candidates) > 0:
                route = candidates[0]
                visited_count = RouteDetailRecord.objects.filter(route=route).count()
                result.append(
                    {"date": date_ago.date().isoformat(), "value": route.total_km, "bin_count": visited_count})
            date_ago += timedelta(days=1)
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return HttpResponse("You cannot POST here.")

# Bir hafta boyunca her gün çöp kutusu başına düşen dolluk oranını yolluyor ; list of lists !!!
def get_last_7_day_per_bin(request):
    if request.method == "GET":
        date_ago = datetime.now() - timedelta(days=7)
        all_bins = Bin.objects.all()
#        bin_count = all_bins.count()
#        result = np.zeros(shape=(7,bin_count))
        result = []
        while date_ago < datetime.now():
            result_day = []
            for bin in all_bins:
                candidates = BinSensorRecord.objects.filter(date__startswith=date_ago.date(), bin__pk=bin.pk).order_by('-date')
                print candidates
                if len(candidates) > 0:
                    record = candidates[0]
                    result_day.append({"date": date_ago.date().isoformat(), "fullness": record.fullness_rate, "bin_id": record.bin_id})
            result.append(result_day)
            date_ago += timedelta(days=1)
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return HttpResponse("You cannot POST here.")

# Bir hafta boyunca kaydedilmiş her forecasting verisini yolluyor !!!
# VARSAYIM : Günde 1 kere Forecasting yapılmış. 1den fazlada sıkıntı çıkabilir.
# TODO: günde 1 den fazla forcasting için düzenle ; fullpipeline tarafı da değişebilir
def get_forecasting_7_day(request):
    if request.method == "GET":
        date_ago = datetime.now() - timedelta(days=7)
        result = []
        while date_ago.day < (datetime.now()).day:
            result_day = []
            candidates = ForecastingRecord.objects.filter(date__startswith=date_ago.date())
            if len(candidates) > 0:
                for record in candidates:
                    result_day.append({"date": date_ago.date().isoformat(), "fullness": record.last_fullness_rate,
                                       "bin_id": record.bin_id, "is_visited": record.is_visited})
            result.append(result_day)
            date_ago += timedelta(days=1)
        return HttpResponse(json.dumps(result), content_type="application*json")
    else:
        return HttpResponse("You cannot POST here.")

# Forecasting sonucunu ForecastingResults tablosuna kaydediyor
@csrf_exempt
def upload_forecasting_results(request):
    if request.method == "GET":
        return HttpResponse("You cannot GET here.")
    else:
        json_data = json.loads(request.body)
        try:
            fill_level_row = json_data['fill_levels']
            visit_row = json_data['visits']
            bin_index_row = json_data['bin_index']
            for i in range(0,len(fill_level_row)):
                bin = Bin.objects.get(pk = bin_index_row[i])
                forecast_result_rec = ForecastingResult(bin=bin, is_visit_predicted=visit_row[i], last_fullness_rate_predicted=fill_level_row[i])
                forecast_result_rec.save()
        except KeyError:
            HttpResponse("Malformed data!")
        return HttpResponse("Got json data")

def get_last_7_day_specific_bin(request, bin_pk=None):
    if request.method == "GET" and bin_pk:
        result = []
        date_ago = datetime.now() - timedelta(days=7)
        our_bin = Bin.objects.get(pk=bin_pk)
        while date_ago <= datetime.now():
            candidates = BinSensorRecord.objects.filter(date__startswith=date_ago.date(), bin__pk=bin_pk).order_by(
                '-date')
            print candidates
            # Her gün için 1 tane (en son) doluluk oranı alarak onu yolluyor.
            if len(candidates) > 0:
                record = candidates[0]
                result.append({"date": date_ago.date().isoformat(), "fullness": record.fullness_rate * 100,
                               "temp": record.temperature})
            date_ago += timedelta(days=1)
        response = {"data": result, "properties": {"coord_lat": our_bin.latitude, "coord_long": our_bin.longitude}}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse("You cannot POST here.")


@csrf_exempt
def input_welcomer(request):
    if request.method == "GET":
        return HttpResponse("You cannot GET here.")
    else:
        cop_id = request.POST.get("cop_id", -1)
        if cop_id != -1:
            try:
                cop = Bin.objects.get(pk=cop_id)
            except Exception as e:
                postlogger.error("ERROR")
                return HttpResponse("Error..\n%s" % str(e))
        else:
            postlogger.error("NO_ID_ERROR")
            return HttpResponse("No cop_id in request..")

        print request.POST

        fullness_rate = min(float(request.POST.get("fl", 0.5)), 1.0)
        battery_rate = float(request.POST.get("bt", random.random()))
        temperature = float(request.POST.get("tmp", random.uniform(19, 22)))
        timestamp = datetime.fromtimestamp(
            int(request.POST.get("ts", str(int(time.mktime(datetime.now().timetuple()))))))

        postlogger.info("%s#%s#%s#%s" % (
            cop_id, fullness_rate, battery_rate, temperature))

        new = BinSensorRecord(bin=cop, fullness_rate=fullness_rate, battery_rate=battery_rate,
                              temperature=temperature, date=timestamp)
        new.save()
        return HttpResponse("Successfully created: %s" % str(new))


@user_passes_test(lambda u: u.is_staff)
def request_logging_page(request):
    return render(request, "dashboard/request_logs.html", {"NO_HEADER": True})


@user_passes_test(lambda u: u.is_staff)
def input_logging_page(request):
    return render(request, "dashboard/input_logs.html", {"bins": Bin.objects.all(), "NO_HEADER": True})

@user_passes_test(lambda u: u.is_staff)
def manage_routing_settings(request):
    return render(request, "dashboard/manage_routing_settings.html", {"vehicles" : Vehicle.objects.all()})

# Ajax
def get_bin_data_specific(request, bin_pk=None):
    if request.method == "GET" and bin_pk:
        bin = Bin.objects.get(pk=bin_pk)
        if bin:
            current = datetime.now()
            records = BinSensorRecord.objects.filter(date__lte=current, bin=bin).order_by('-date')
            processed = [{"fullness_rate": x.fullness_rate, "timestamp": x.date_as_timestamp} for x in records]
            # print processed
            return HttpResponse(json.dumps(processed), content_type="application/json")
        return HttpResponse("[]", content_type="application/json")
    else:
        return HttpResponse("You cannot POST here.")

# Sensor config setter
# URL = localhost:8000/routing/get_cfg/sensor_id
# URL_REAL = evreka.co/routing/get_cfg/sensor_id
def get_sensor_cfg(request, sensor_id=None):
    if request.method == "GET" and sensor_id:
        try:
            bin = Bin.objects.get(sensor_id=sensor_id)
            connection_freq = bin.connection_freq
            measurement_freq = bin.measurement_freq
            result = "%s,%s" %(connection_freq,measurement_freq)
            print result
            return HttpResponse(result)
        except:
            print "Bin-Sensor Asignment"
            candidates = Bin.objects.filter(sensor_id="X")
            target_bin = candidates[0]
            print "Assigned Bin ID: %s" % target_bin.bin_id
            print "Assigned Sensor ID: %s" % sensor_id
            target_bin.sensor_id = sensor_id
            target_bin.save()
            connection_freq = target_bin.connection_freq
            measurement_freq = target_bin.measurement_freq
            result = "%s,%s" %(connection_freq,measurement_freq)
            print result
            return HttpResponse(result)
    else:
        return HttpResponse("You cannot POST here")

# Ajax/Direct Get request
def get_bin_data_details_all(request):
    if request.method == "GET":
        bins = Bin.objects.all()
        processed = [{"fullness_rate": x.current_record.fullness_rate, "latitude": x.latitude, "longitude": x.longitude,
                      "bin_id": int(x.bin_id)} for x in bins]
        processed.sort(key=lambda x: x["bin_id"])
        return HttpResponse(json.dumps(processed), content_type="application/json")
    else:
        return HttpResponse("You cannot POST here.")


@csrf_exempt
def upload_route(request):
    if request.method == "GET":
        print "GET", request.GET
        return HttpResponse("Get..")
    else:
        print "POST", request.POST
        print "FILES", request.FILES
        bins_on_tour = request.POST['bin_string']
        bins_splitted = map(int,bins_on_tour.split())
        fname_splitted = request.FILES['processed_kml_file'].name.split("_")
        timestamp = datetime.fromtimestamp(int(fname_splitted[0]))
        vehicle_index = int(fname_splitted[1])
        vehicles = Vehicle.objects.all()
        print vehicle_index, fname_splitted[0], timestamp
        if vehicles.count() > vehicle_index:
            form = RouteUploadForm(data=request.POST, files=request.FILES)
            print form
            if form.is_valid():
                model_instance = form.save()
                model_instance.vehicle = vehicles[vehicle_index]
                model_instance.date = timestamp
                model_instance.save()

                route = Route.objects.get(date = timestamp)
                for bin_id in bins_splitted:
                    bin = Bin.objects.get(bin_id = bin_id)
                    try:
                        detail_exist = RouteDetailRecord.objects.get(bin=bin, route = route)
                        print "Bin ID : %s , is already exist on Route: %s " %(bin,route)
                        print "Detail Record ID: %s" %detail_exist.detail_id
                    except:
                        detail = RouteDetailRecord(bin = bin, route = route)
                        detail.save()
                return HttpResponse("Route Saved Succesfully")
            else:
                print form.errors
                print form.non_field_errors()
                return HttpResponse("Error at route saving" + "\n" + str(form.errors))
        else:
            return HttpResponse("No enough vehicle to save route")
