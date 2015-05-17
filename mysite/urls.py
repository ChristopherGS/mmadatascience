from django.conf.urls import include, patterns, url
from django.contrib import admin

#from . import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('ufc.urls', namespace="ufc")),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^`$', mysite.views.home),
    url(r'^searches/', include('ufc.urls', namespace="ufc")),
	url(r'^ufc/', include('ufc.urls', namespace="ufc")),
	url(r'^admin/', include(admin.site.urls)),
)
