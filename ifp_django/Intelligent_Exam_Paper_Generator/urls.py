from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Intelligent_Exam_Paper_Generator.views.home', name='home'),
    # url(r'^Intelligent_Exam_Paper_Generator/', include('Intelligent_Exam_Paper_Generator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documyesentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    #url(r'^tinymce/', include('tinymce.urls')),
    # admin-tools
    url(r'^admin_tools/', include('admin_tools.urls')),

    # end of admin-tools
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    )
