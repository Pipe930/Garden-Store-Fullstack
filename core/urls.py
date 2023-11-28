from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.products.urls import urlsCategories, urlsProducts, urlsOffers
from apps.users.urls import urlsSubcriptions
from apps.countries.urls import urlsRegions, urlsProvincies, urlsCommunes
from apps.sales.urls import urlsCarts, urlsVouchers
from apps.branchs.urls import urlsBranchs

urls_api =  [
    path("categories/", include(urlsCategories)),
    path("products/", include(urlsProducts)),
    path("offers/", include(urlsOffers)),
    path("subscriptions/", include(urlsSubcriptions)),
    path("regions/", include(urlsRegions)),
    path("provinces/", include(urlsProvincies)),
    path("communes/", include(urlsCommunes)),
    path("carts/", include(urlsCarts)),
    path("vouchers/", include(urlsVouchers)),
    path("branchs/", include(urlsBranchs)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt"))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1.0/", include(urls_api))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'
