from django.contrib import admin
from django.urls import path, include
from chat import urls as chat_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(chat_urls)),
]


