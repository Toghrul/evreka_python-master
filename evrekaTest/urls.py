from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^mapbox/$', 'evrekaTest.views.kml_test_mapbox'),
    url(r'^osm/$', 'evrekaTest.views.kml_test'),
    url(r'^vehicles/$', 'evrekaTest.views.dashboard_vehicles'),
    url(r'^bin/$', 'evrekaTest.views.dashboard_bins'),
    url(r'^logs/input$', 'evrekaTest.views.input_logging_page'),
    url(r'^logs/request$', 'evrekaTest.views.request_logging_page'),
    url(r'^manage', 'evrekaTest.views.manage_routing_settings'),



    #Ajax
    url(r'^get_kml', 'evrekaTest.views.get_kml'),
    url(r'^selam', 'evrekaTest.views.selam'),
    url(r'^post', 'evrekaTest.views.vehiclepost'),
    url(r'^yeni', 'evrekaTest.views.yeni'),
    url(r'^get_last_7_day_all', 'evrekaTest.views.get_last_7_day_all'),
    url(r'^get_last_7_day_bin_fullness', 'evrekaTest.views.get_last_7_day_bin_fullness'),
    url(r'^get_last_7_day_per_bin', 'evrekaTest.views.get_last_7_day_per_bin'),
    url(r'^get_forecast_7_day', 'evrekaTest.views.get_forecasting_7_day'),
    url(r'^get_last_7_day_specific_vehicle/(?P<vehicle_pk>\d+)/$', 'evrekaTest.views.get_last_7_day_specific_vehicle'),
    url(r'^get_last_7_day_specific_bin/(?P<bin_pk>\d+)/$', 'evrekaTest.views.get_last_7_day_specific_bin'),

    url(r'^get_bin_data/(?P<bin_pk>\d+)/$', 'evrekaTest.views.get_bin_data_specific'),
    url(r'^get_latest_bins_data/$', 'evrekaTest.views.get_bin_data_details_all'),

    #Data outcome
    url(r'^get_cfg/(?P<sensor_id>\w+)/$', 'evrekaTest.views.get_sensor_cfg'),

    #Data income
    url(r'^input', 'evrekaTest.views.input_welcomer'),
    url(r'^send_route_file', 'evrekaTest.views.upload_route'),
    url(r'^send_forecast_result', 'evrekaTest.views.upload_forecasting_results'),


    url(r'^$', 'evrekaTest.views.dashboard_home'),
)
