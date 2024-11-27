from django.urls import path, include
from chat import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers


router = routers.SimpleRouter()
router.register('messages', views.MessageViewSet)
router.register('rooms', views.RoomViewSet)
router.register(r'rooms/(?P<room_id>\d+)/messages', views.RoomMessageViewSet, basename='roommessage')
router.register('users', views.UserViewSet, basename='users')

auth_patterns = [
    path('tokens/', obtain_auth_token),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_patterns)),
]

