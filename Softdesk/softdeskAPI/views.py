from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from .models import MyUser
from .serializers import MyUserSerializer


class CreateUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyUserSerializer


class ListUserAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()




