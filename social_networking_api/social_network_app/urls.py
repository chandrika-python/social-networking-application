from .views import RegisterView, LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search-users/', UserSearchView.as_view(), name='search-users'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
    path('friend-requests/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-requests/<int:pk>/accept/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-requests/<int:pk>/reject/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('', include(router.urls)),
]