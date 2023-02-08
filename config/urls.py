from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("pay_right_here.accounts.urls")),
    path("api/v1/jwtauth/", include("pay_right_here.jwtauth.urls")),
    path("api/v1/accountbooks/", include("pay_right_here.accountbook.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
