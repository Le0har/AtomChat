from django.contrib import admin
from django.urls import path, include
from chat import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers


router = routers.SimpleRouter()
router.register('messages', views.MessageViewSet)
router.register('rooms', views.RoomViewSet)
router.register(r'rooms/(?P<room_id>\d+)/messages', views.RoomMessageViewSet, basename='roommessage')
router.register('auth/register', views.UserCreateSet, basename='register')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/messages/', views.MessageViewSet.as_view({'post': 'create'})),
#     path('api/rooms/', views.RoomViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('api/rooms/<int:room_id>/', views.RoomViewSet.as_view({'put': 'update', 'get': 'list', 'delete': 'destroy'})),
#     path('api/rooms/<int:room_id>/messages/', views.RoomMessageViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('api-token-auth/', obtain_auth_token),
#     path('api/auth/register/', views.UserCreateSet.as_view({'post': 'create'})),
# ]
