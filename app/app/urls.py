from django.contrib import admin
from django.urls import path
from chat import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/messages/getlist/', views.MessageViewSet.as_view({'get': 'list'})),
    path('api/messages/', views.MessageViewSet.as_view({'post': 'create'})),
]
