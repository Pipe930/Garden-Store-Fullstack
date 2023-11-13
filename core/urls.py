from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.products.urls import urlsCategories, urlsProducts

urls_api =  [
    path("categories/", include(urlsCategories)),
    path("products/", include(urlsProducts))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1.0/", include(urls_api)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
