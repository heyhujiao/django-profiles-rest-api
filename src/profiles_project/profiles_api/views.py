from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions


# Create your views here.

class HelloApiView(APIView):
    """
    Test API View
    """

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """
        Returns a list of APIView features
        :param request:
        :param format:
        :return:
        """

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)'
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'is mapped manually to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """
        Create a Hello message with our name
        :param request: Object
        :return: JSON
        """

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Handles updating an object
        :param request:
        :param pk:
        :return:
        """
        # pk refers to the primary key
        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """
        Patch request, only updates fields provided in the request
        :param request:
        :param pk:
        :return:
        """
        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """
        Deletes an object
        :param request:
        :param pk:
        :return:
        """
        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """
    test API viewset
    """

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """
        return a hello message
        :param request:
        :return:
        """

        a_viewset = [
            'Uses actions(list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using routers',
            'Provides more functionalities with less code'
        ]

        return Response({'message': "hello!", 'a_viewset': a_viewset})

    def create(self, request):
        """
        create a new hello message
        :param request:
        :return:
        """
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """
        Handles getting an object by its ID
        :param request:
        :param pk:
        :return:
        """
        return Response({'http method': 'GET'})

    def update(self, request, pk=None):
        """
        handles updating an object
        :param request:
        :param pk:
        :return:
        """

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """
        Handles updating part of an object
        :param request:
        :param pk:
        :return:
        """
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """
        handles removing an object
        :param request:
        :param pk:
        :return:
        """

        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Handles creating, reading and updating profiles
    """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """
    Checks email and password and returns an auth token
    """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        Use the ObtainAuthToken APIView to validate and create a token
        :param request:
        :return:
        """

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """
    Handles creating, reading and updating profile feed items
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Sets the user profile to the logged in user
        :param serializer:
        :return:
        """
        serializer.save(user_profile=self.request.user)
