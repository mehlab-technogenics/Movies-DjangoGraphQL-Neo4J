from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Profile
import datetime
from .serializers import ProfileSerializer,UserSerializer

def dashboard(request):
    return render(request, "users/dashboard.html")




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLoguser(request):
    data=request.user
    project = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(project, many=False)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    print(request.user)
    websites = Profile.objects.all()
    serializer = ProfileSerializer(websites, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_auth(request):
    print('Hello')
    print(request.data)
    user = User.objects.create_user(username=request.data['username'],
                                 email=request.data['email'],
                                 password=request.data['password'])
    profile=Profile.objects.create(user=user,name=request.data['username'],email=request.data['email'])
    #serializer = UserSerializer(data=request.data)
    serializer = ProfileSerializer(profile, many=False)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)