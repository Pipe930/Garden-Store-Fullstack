from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.products.urls import urlsCategories, urlsProducts, urlsOffers, urlsStore
from apps.users.urls import urlsUsers, urlsSubcriptions
from apps.countries.urls import urlsRegions, urlsProvincies, urlsCommunes
from apps.sales.urls import urlsCarts, urlsVouchers

urls_api =  [
    path("categories/", include(urlsCategories)),
    path("products/", include(urlsProducts)),
    path("offers/", include(urlsOffers)),
    path("users/", include(urlsUsers)),
    path("subscriptions/", include(urlsSubcriptions)),
    path("regions/", include(urlsRegions)),
    path("provinces/", include(urlsProvincies)),
    path("communes/", include(urlsCommunes)),
    path("carts/", include(urlsCarts)),
    path("vouchers/", include(urlsVouchers)),
    path("stores/", include(urlsStore))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1.0/", include(urls_api))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
