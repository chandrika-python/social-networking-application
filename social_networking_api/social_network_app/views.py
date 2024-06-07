from rest_framework.permissions import AllowAny
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import UsersModel, FriendRequestModel
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from rest_framework.pagination import PageNumberPagination


class UserSearchPagination(PageNumberPagination):
    page_size = 10


class UserSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('search', '')
        if '@' in keyword:
            return UsersModel.objects.filter(email__iexact=keyword)
        return UsersModel.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))


class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequestModel.objects.filter(to_user=self.request.user, status='pending')


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        try:
            to_user = UsersModel.objects.get(id=to_user_id)
        except UsersModel.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        from_user = request.user

        # Rate limit: no more than 3 requests per minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequestModel.objects.filter(from_user=from_user,
                                                                  time_stamp__gte=one_minute_ago).count()
        if recent_requests_count >= 3:
            return Response({'error': 'Rate limit exceeded. Please wait a moment before sending more requests.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request, created = FriendRequestModel.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequestModel.objects.all()
    serializer_class = FriendRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'accepted'
        instance.save()
        return Response(FriendRequestSerializer(instance).data)


class RejectFriendRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequestModel.objects.all()
    serializer_class = FriendRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'rejected'
        instance.save()
        return Response(FriendRequestSerializer(instance).data)


class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = UsersModel.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status='accepted') |
            Q(received_requests__from_user=user, received_requests__status='accepted')
        ).distinct()
        return friends


class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequestModel.objects.filter(to_user=self.request.user, status='pending')


class RegisterView(generics.CreateAPIView):
    queryset = UsersModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful',
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            logout(request)
            data = {'success': 'Sucessfully logged out'}
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
