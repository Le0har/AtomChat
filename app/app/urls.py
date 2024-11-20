from django.contrib import admin
from django.urls import path
from chat import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/messages/', views.MessageViewSet.as_view({'post': 'create'})),
    path('api/rooms/', views.RoomViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/rooms/<int:room_id>/messages/', views.RoomMessageViewSet.as_view({'get': 'list', 'post': 'create'})),
]
