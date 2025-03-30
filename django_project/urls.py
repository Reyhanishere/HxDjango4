from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("pages.urls")),
    path("cases/", include("cases.urls")),
    path("calculus/", include("calculus.urls")),

    path("blog/",include("blogs.urls")),
    path("docs/",include("docs.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
