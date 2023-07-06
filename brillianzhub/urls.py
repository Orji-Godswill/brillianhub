from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', views.index_view, name="home"),
    path('accounts/', include("accounts.passwords.urls")),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include("accounts.urls", namespace="account")),
    path('settings/', RedirectView.as_view(url='/account')),
    path('admin/', admin.site.urls),

    path('financial-investment/', include("blog.urls")),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('contact/', views.contact_view, name="contact"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
