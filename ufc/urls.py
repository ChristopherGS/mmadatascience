from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^search/$', views.search),
	url(r'^search/results/$', views.results),
	url(r'^searches/all-searches/$', views.view_list),
	url(r'^searches/new/$', views.new_search),
	url(r'^soup/$', views.beautiful_soup),
]