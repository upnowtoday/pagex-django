from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.views import APIViewMixin
from .serializers import UserDetailSerializer, FollowSerializer
from .models import Passion

User = get_user_model()


class LoggedInUserAPI(APIView, APIViewMixin):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, context=self.get_serializer_context())
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True, context=self.get_serializer_context())
        serializer.is_valid(True)
        serializer.save()
        return Response(serializer.data)


class UserAPI(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'user_id'


class PassionListView(APIView):
    queryset = Passion.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        passion_list = self.queryset.values_list('name', flat=True)
        return Response({'passion': passion_list})


class FollowAPI(APIView, APIViewMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def post(self, request, user_id, follow_type, *args, **kwargs):
        serializer = self.serializer_class(data={'followee': user_id, 'follow_type': follow_type}, context=self.get_serializer_context())
        serializer.is_valid(True)
        getattr(serializer, follow_type)()
        return Response({'detail': f'Successfully {follow_type}ed'})
