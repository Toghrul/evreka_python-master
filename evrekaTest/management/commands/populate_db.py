# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from evrekaTest.models import Bin, BinSensorRecord, RouteDetailRecord, Route, Vehicle, ClientRecord, ForecastingRecord#, BinVisitHistory, NavigationRecord
import numpy as np
from random import randint, random, uniform, choice
np.random.seed(42)

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def get_fullness_ratio(self, nb_of_containers, nb_of_periods, threshold):
        daily_amounts = np.random.random((nb_of_containers, nb_of_periods))
        daily_amounts = np.concatenate([daily_amounts, np.zeros((nb_of_containers, 1))], axis=1)
        daily_amounts = np.cumsum(daily_amounts, axis=1)
        visited = np.zeros((nb_of_containers, nb_of_periods))
        for i in range(nb_of_periods):
            should_visit = daily_amounts[..., i+1] > threshold

            visited[..., i] = should_visit

            d = np.tile(daily_amounts[..., i] * should_visit, (nb_of_periods+1, 1)).T
            d[..., :i+1] = 0

            daily_amounts -= d

        return daily_amounts[..., :-1], visited

    def handle(self, ndays=7, *args, **options):
#        BinVisitHistory.objects.all().delete()
#        NavigationRecord.objects.all().delete()
        ForecastingRecord.objects.all().delete()
        BinSensorRecord.objects.all().delete()
        RouteDetailRecord.objects.all().delete()
        Route.objects.all().delete()
        Bin.objects.all().delete()
        Vehicle.objects.all().delete()
        ClientRecord.objects.all().delete()

        print "-Database is cleared, Starts Client Creation"
        c1 = ClientRecord(client_name="Beypazarı Belediyesi")
        c1.save()
        print "+Client Creation is SUCCESSFULL"
        print "-Starts Vehicle creation"
        v1 = Vehicle(vehicle_id=1,client=c1, plate="06 JM 1452")
        v2 = Vehicle(vehicle_id=2,client=c1, plate="06 TM 1682")
        v3 = Vehicle(vehicle_id=3,client=c1, plate="06 PK 1298")
        print "+Vehicle Records created SUCCESSFULLY"
        v1.save()
        v2.save()
        v3.save()
        print "-Starts Bin Record creation"
        with open("templates/sample_kml/algoritma_input.csv", "r") as f:
            f.readline()
            for idx, line in enumerate(f):
                splitted = line.split(",")
                if idx==0:
                    idx = 3168
                new_bin = Bin(bin_id=str(idx),client=c1, latitude=splitted[0], longitude=splitted[1])
                new_bin.save()
        bin_count = Bin.objects.all().count()
        print bin_count
        date_ago = datetime.now() - timedelta(days=ndays)
        date_now = datetime.now()
        fill_level, visit_history = self.get_fullness_ratio(bin_count, ndays+1, 0.8)

        print "+Bin Records created SUCCESSFULLY"
        print "-Starts SensorRecord creation"
        j=0
        while date_ago <= date_now:
            i=0
            all_bins = Bin.objects.all()
            for bin in all_bins:
                d = datetime(year=date_ago.year, month=date_ago.month, day= date_ago.day, hour=0, minute=1)
                rec = BinSensorRecord(bin=bin, fullness_rate=fill_level[i][j], battery_rate=uniform(0.75, 0.95),
                                      temperature=uniform(18.0, 21.0), date=d)
                rec.save()
                if j < ndays:
                     rec_for = ForecastingRecord(bin=bin, is_visited=visit_history[i][j],date=d,last_fullness_rate=fill_level[i][j])
                     rec_for.save()
                i=i+1
            j = j+1
            date_ago = date_ago + timedelta(days=1)

        date_ago = datetime.now() - timedelta(days=7)
        date_now = datetime.now()

        print "+SensorRecords created SUCCESSFULLY"
        print "-Starts Route,Route Detail and Visit History creation for a week"
        while date_ago <= date_now:
            kml_files_arac_1 = ['arac1_1.kml', 'arac1_2.kml', 'arac1_3.kml', 'arac1_4.kml']
            kml_files_arac_2 = [ 'arac2_1.kml', 'arac2_2.kml', 'arac2_3.kml', 'arac2_4.kml']
            kml_files_arac_3 = ['arac3_1.kml', 'arac3_2.kml']


            route1 = Route(date=date_ago, duration=uniform(60.0, 90.0), total_km=uniform(20.0, 50.0), vehicle=v1,
                           processed_kml_file='/media/' + choice(kml_files_arac_1))
            route2 = Route(date=date_ago, duration=uniform(60.0, 90.0), total_km=uniform(20.0, 50.0), vehicle=v2,
                           processed_kml_file='/media/' + choice(kml_files_arac_2))
            route3 = Route(date=date_ago, duration=uniform(60.0, 90.0), total_km=uniform(20.0, 50.0), vehicle=v3,
                           processed_kml_file='/media/' + choice(kml_files_arac_3))
            routes = [route1, route2, route3]

            route1.save()
            route2.save()
            route3.save()

            all_bins = Bin.objects.all()
            for bin in all_bins:
                if random() < 0.75:
                    cur_route = choice(routes)
                    rec = RouteDetailRecord(bin=bin, route=cur_route)
                    rec.save()

            date_ago = date_ago + timedelta(days=1)
            print "Day is Finished"
        print "+Population is finished"