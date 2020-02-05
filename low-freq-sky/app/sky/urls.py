from django.conf.urls import url
from django.contrib import admin
from sky import views

admin.autodiscover()

urlpatterns = [
    url(r'^(?P<observatory>\w*)/(?P<datetime>\d{4}/\d{2}/\d{2}/\d{2}:\d{2}:\d{2})(?P<timezone>[-+]\d{4})/$',  views.sky_all, {'template_name': 'sky_table1.html'}),
]
