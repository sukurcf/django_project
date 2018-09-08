from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.conf.urls import url
from django_project import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('djangobin.urls'))
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)