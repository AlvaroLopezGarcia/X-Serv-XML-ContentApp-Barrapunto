from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'cms.views.barra'),
    url(r'^pages/(\d+)$','cms.views.pages'),
    url(r'^update/','cms.views.update'),
    url(r'^admin/', include(admin.site.urls)),
)
