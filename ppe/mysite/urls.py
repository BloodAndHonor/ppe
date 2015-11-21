from django.conf.urls import patterns, include, url
from django.contrib import admin
import mysite.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ppe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/', mysite.views.login, name='login'),
    url(r'^logout/', mysite.views.logout, name='logout'),
    url(r'^init/', mysite.views.init),
    url(r'^$', mysite.views.index, name='index'), 
    url(r'^up_dev/', mysite.views.upload_device, name='up_dev'), 
    url(r'^up_chg/', mysite.views.upload_change, name='up_chg'), 
    url(r'^s/', mysite.views.dev_s, name="s")
)
