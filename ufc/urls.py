from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^soup/(?P<fighter>[-\w]{0,50})/(?P<sherdog_id>[-\w]{0,50})/$', views.beautiful_soup, name='scrape'),
	url(r'^fighter/query/$', views.hunt),
	url(r'^organize/$', views.organize),
]
