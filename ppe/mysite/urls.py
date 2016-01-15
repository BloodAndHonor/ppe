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
    url(r'^chpass/', mysite.views.chg_pass, name='chpass'), 
    url(r'^s/', mysite.views.dev_s, name='s'),
    url(r'^chg_s/', mysite.views.chg_s, name='chg_s'),
    url(r'^chg/', mysite.views.chg, name='chg'), 
    url(r'^ex/', mysite.views.export_dev, name='export'), 
    url(r'^t/', mysite.views.auto_aban), 
    url(r'^chg_config/', mysite.views.chg_config, name='chg_config'), 
    url(r'^aban/', mysite.views.aban, name='aban'),
    url(r'^fact/', mysite.views.fact_number, name='fact_num')
)
