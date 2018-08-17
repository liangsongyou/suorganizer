from django.conf.urls import include, url
from django.contrib import admin


from organizer.views import homepage, tag_detail

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', homepage),
    url(r'^tag/(?P<slug>[\w\-]+)/$', 
        tag_detail,
        name='organizer_tag_detail'),
]
