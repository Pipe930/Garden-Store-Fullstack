from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.products.urls import urls_categories, urls_products
from apps.users.urls import urls_subcriptions, urls_users
from apps.countries.urls import urls_communes, urls_provincies, urls_regions
from apps.sales.urls import urls_carts, urls_vouchers
from apps.branchs.urls import urls_branchs
from apps.admin.urls import urls_administration
from apps.users.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urls_jwt = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("refresh", TokenRefreshView.as_view(), name="refresh_token")
]

urls_api =  [
    path("categories/", include(urls_categories)),
    path("products/", include(urls_products)),
    path("subscriptions/", include(urls_subcriptions)),
    path("regions/", include(urls_regions)),
    path("provinces/", include(urls_provincies)),
    path("communes/", include(urls_communes)),
    path("carts/", include(urls_carts)),
    path("vouchers/", include(urls_vouchers)),
    path("branchs/", include(urls_branchs)),
    path("users/", include(urls_users)),
    path("admin/", include(urls_administration)),
    path("auth/", include("djoser.urls")),
    path("auth/jwt/", include(urls_jwt))
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
