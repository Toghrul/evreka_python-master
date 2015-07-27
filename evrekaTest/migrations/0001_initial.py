# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bin',
            fields=[
                ('bin_id', models.IntegerField(serialize=False, verbose_name=b'Bin ID', primary_key=True)),
                ('sensor_id', models.CharField(default=b'X', max_length=200)),
                ('latitude', models.FloatField(verbose_name=b'Lat.')),
                ('longitude', models.FloatField(verbose_name=b'Long.')),
                ('info', models.TextField(null=True, verbose_name=b'Info', blank=True)),
                ('size', models.FloatField(default=1, verbose_name=b'Size of Bin')),
                ('measurement_freq', models.IntegerField(default=8, verbose_name=b'Measurement (times per connection)')),
                ('connection_freq', models.IntegerField(default=480, verbose_name=b'Connection Frequency (in minutes) ')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BinSensorRecord',
            fields=[
                ('SensRecord_id', models.AutoField(serialize=False, verbose_name=b'Sensor Record ID', primary_key=True)),
                ('fullness_rate', models.FloatField(verbose_name=b'Fullness Rate')),
                ('battery_rate', models.FloatField(verbose_name=b'Battery Rate')),
                ('temperature', models.FloatField(verbose_name=b'Temperature')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Record Date', blank=True)),
                ('is_working', models.BooleanField(default=True, verbose_name=b'Sensors Working')),
                ('bin', models.ForeignKey(to='evrekaTest.Bin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientRecord',
            fields=[
                ('client_id', models.AutoField(serialize=False, verbose_name=b'Client ID', primary_key=True)),
                ('client_name', models.CharField(default=b'-', max_length=30)),
                ('info', models.TextField(null=True, verbose_name=b'Info', blank=True)),
                ('jsonfile', models.FileField(upload_to=b'', null=True, verbose_name=b'JSON File', blank=True)),
                ('duration_matrix_txt', models.FileField(upload_to=b'', null=True, verbose_name=b'Duration Matrix TXT', blank=True)),
                ('distance_matrix_txt', models.FileField(upload_to=b'', null=True, verbose_name=b'Distance Matrix TXT', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForecastingRecord',
            fields=[
                ('forecast_id', models.AutoField(serialize=False, verbose_name=b'Forecasting ID', primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Date')),
                ('is_visited', models.BooleanField(default=False, verbose_name=b'Visit Status on Field')),
                ('last_fullness_rate', models.FloatField(verbose_name=b'Fullness Rate Before Routing')),
                ('bin', models.ForeignKey(to='evrekaTest.Bin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForecastingResult',
            fields=[
                ('result_id', models.AutoField(serialize=False, verbose_name=b'Prediction ID', primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Prediction Date')),
                ('is_visit_predicted', models.BooleanField(default=True, verbose_name=b'Visit Status on Prediction')),
                ('last_fullness_rate_predicted', models.FloatField(verbose_name=b'Predicted Rate for Future')),
                ('bin', models.ForeignKey(to='evrekaTest.Bin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestErrorLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=30)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(null=True, verbose_name=b'date', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('route_id', models.AutoField(serialize=False, verbose_name=b'Route ID', primary_key=True)),
                ('processed_kml_file', models.FileField(upload_to=b'', null=True, verbose_name=b'Route KML file (generated)', blank=True)),
                ('real_kml_file', models.FileField(upload_to=b'', null=True, verbose_name=b'Route KML file (GPS data)', blank=True)),
                ('duration', models.FloatField(default=0.0, verbose_name=b'Duration', blank=True)),
                ('total_km', models.FloatField(default=0.0, verbose_name=b'Total KM', blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Date', blank=True)),
                ('assign_date', models.DateTimeField(null=True, verbose_name=b'Assignment Date', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RouteDetailRecord',
            fields=[
                ('detail_id', models.AutoField(serialize=False, verbose_name=b'Route Detail ID', primary_key=True)),
                ('bin', models.ForeignKey(to='evrekaTest.Bin')),
                ('route', models.ForeignKey(to='evrekaTest.Route')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('vehicle_id', models.AutoField(serialize=False, verbose_name=b'Vehicle ID', primary_key=True)),
                ('fuel_consumption', models.FloatField(default=10, verbose_name=b'Fuel Consumption per 100 km (in litres)')),
                ('plate', models.CharField(default=b'', max_length=10, verbose_name=b'Plate')),
                ('number_of_trip', models.IntegerField(default=1)),
                ('capacity', models.FloatField(default=0, verbose_name=b'Vehicle Capacity to store waste in meter cube')),
                ('work_time', models.FloatField(default=0, verbose_name=b'Time to work per day in minutes')),
                ('use_for_routing', models.BooleanField(default=False)),
                ('client', models.ForeignKey(to='evrekaTest.ClientRecord')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='route',
            name='vehicle',
            field=models.ForeignKey(blank=True, to='evrekaTest.Vehicle', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bin',
            name='client',
            field=models.ForeignKey(to='evrekaTest.ClientRecord'),
            preserve_default=True,
        ),
    ]
