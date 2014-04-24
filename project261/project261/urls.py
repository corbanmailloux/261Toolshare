"""
File:       project261/project261/urls.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

All of the different urls for all of the different types of pages
in this toolshare project.
"""

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/old/', include(admin.site.urls)),
    url(r'^postman/', include('postman.urls')), # DO NOT NAMESPACE THIS IT BREAKS ALL THE THINGS
    
    #include set of URLs in toolshare, at top level
    url(r'^', include('toolshare.urls', namespace="toolshare")), 
    
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^login/$', 'project261.views.login', name='login'),
    url(r'^logout/$', 'project261.views.logout', name='logout'),
    url(r'^register/$', 'project261.views.register', name='register'),

    #password change
    url(r'^password/change$', 'django.contrib.auth.views.password_change', {'template_name': 'registration/password/password_change_form.html'}, name="password_change"),
    url(r'^password/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'registration/password/password_change_done.html'}, name="password_change_done"),

    #password reset
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'registration/password/password_reset_form.html'}, name='password_reset'),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'registration/password/password_reset_done.html'}),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'registration/password/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'registration/password/password_reset_complete.html'}),
)
