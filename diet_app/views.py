from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.db import IntegrityError
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from diet_app.serializers import *

from diet_app.models import *


class DiaryView(APIView):
    def get(self, request):
        serializer = DiarySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(serializer.data)


class ActivityView(APIView):
    def get(self, request):
        serializer = ActivityGetSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActivityCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(serializer.data)

    def delete(self, request):
        serializer = ActivityDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete(serializer.validated_data)
        return Response(serializer.data)

# LIST OF DICTIONARIES - TODO
# class ActivitiesView(APIView):
#     def get(self, request, format=None):
#         serializer = ActivitiesListSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data)


class ProductView(APIView):
    def get(self, request):
        serializer = ProductGetSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid()
        serializer.create(serializer.validated_data)
        return Response(serializer.data)

# LIST OF DICTIONARIES AND SEARCHING - TODO
# class ProductsView(APIView):
#     def get(self, request):
#         serializer = ProductsGetSerializer(data=request.query_params)
#         serializer.is_valid()
#         return Response(serializer.data)




