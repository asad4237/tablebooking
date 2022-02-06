from django.shortcuts import render
from django.utils.dateparse import parse_date
from rest_framework import viewsets
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from restaurants.serializers import BookingSerializer, RestaurantSerializer, TableSerializer, BookingSerializerGET
from restaurants.models import Booking, Restaurant, Table
from restaurants import booking
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .permission import IsAdminOrEmployeeUser, IsAdminUser


class BookinngViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows booking to be viewed/created/edited/deleted.
    """
    queryset = Booking.objects.all().order_by('id')
    serializer_class = BookingSerializer
    update_data_pk_field = 'id'

    def get_permissions(self):
        permission_classes = []
        allowany = True
        if self.action == 'create':
            if not allowany:
                permission_classes = [IsAdminOrEmployeeUser]
        elif self.action == 'list':
            if not allowany:
                permission_classes = [IsAdminOrEmployeeUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            if not allowany:
                permission_classes = [IsAdminOrEmployeeUser]
        elif self.action == 'destroy':
            if not allowany:
                permission_classes = [IsAdminOrEmployeeUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        if self.request.method == "GET" or self.request.method == "PUT" or self.request.method == "PATCH":
            return BookingSerializerGET
        return BookingSerializer

    def create(self, request, *args, **kwargs):
        #kwarg_field: str = self.lookup_url_kwarg or self.lookup_field
        #self.kwargs[kwarg_field] = request.data[self.update_data_pk_field]

        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                from datetime import datetime
                booking_date_time_start = datetime.strptime(serializer['booking_date_time_start'].value, '%Y-%m-%dT%H:%M:%S%z')
                booking_date_time_end = datetime.strptime(serializer['booking_date_time_end'].value, '%Y-%m-%dT%H:%M:%S%z')

                booking_response = booking.book_restaurant_table(
                    restaurant=serializer['restaurant'].value,
                    booking_date_time=booking_date_time_start,
                    booking_date_time_end=booking_date_time_end,
                    people=serializer['people'].value)
                if booking_response is None:
                    return Response({"status": "booking not available", "data": "Booking not available for the selected datetime and selected number of people. Try changing number of people or datetime."},
                                    status=status.HTTP_404_NOT_FOUND)

                return Response({"status": " create booking success", "data": booking_response}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error booking", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": "error booking", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows booking to be viewed/created/edited/deleted.
    """
    queryset = Restaurant.objects.all().order_by('name')
    serializer_class = RestaurantSerializer
    update_data_pk_field = 'name'

    def create(self, request, *args, **kwargs):
        kwarg_field: str = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[kwarg_field] = request.data[self.update_data_pk_field]
        serializer = RestaurantSerializer(data=request.data)
        print('inside create of view')
        if serializer.is_valid():
            try:
                self.update(request, *args, **kwargs)
                return Response({"status": "update success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Http404:
                super().create(request, *args, **kwargs)
                return Response({"status": " create success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        serializer = RestaurantSerializer(data=request.data)
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"status": "delete success", "data": {}}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "delete error", "data": e}, status=status.HTTP_204_NO_CONTENT)


class TableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows booking to be viewed/created/edited/deleted.
    """
    queryset = Table.objects.all().order_by('size')
    serializer_class = TableSerializer
    update_data_pk_field = 'id'

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        #if request.method == 'DELETE':
            #kwarg_field: str = self.lookup_url_kwarg or self.lookup_field
           # self.kwargs[kwarg_field] = request.data[self.update_data_pk_field]

        serializer = TableSerializer(data=request.data)

        if serializer.is_valid():
            try:
                super().create(request, *args, **kwargs)
                return Response({"status": "create table success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": " error", "data": e}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        serializer = TableSerializer(data=request.data)
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"status": "delete success", "data": {}}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "delete error", "data": {}}, status=status.HTTP_204_NO_CONTENT)
