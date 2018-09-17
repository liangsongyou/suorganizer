from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import urls as flatpages_urls


from blog import urls as blog_urls
from .views import redirect_root
from contact import urls as contact_urls
from organizer.urls import (
    newslink as newslink_urls,
    startup as startup_urls,
    tag as tag_urls)

urlpatterns = [
    
    url(r'^newslink/', include(newslink_urls)),
    url(r'^startup/', include(startup_urls)),
    url(r'^tag/', include(tag_urls)),
    url(r'^contact/', include(contact_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog_urls)),
    url(r'^$', redirect_root),
    url(r'^', include(flatpages_urls)),
    # url(r'^', include(organizer_urls)),
    
]
