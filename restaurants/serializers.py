from datetime import datetime

from rest_framework import serializers
from .models import Booking, Restaurant, Table
from restaurants import booking


class BookingSerializer(serializers.Serializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    booking_date_time_start = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    booking_date_time_end = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    people = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ['id','restaurant','booking_date_time_start', 'booking_date_time_end', 'people']
        extra_kwargs = {'people': {'required': True}}
        ordering = ('id',)


class BookingSerializerGET(serializers.Serializer):
    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())
    booking_date_time_start = serializers.DateTimeField()
    booking_date_time_end = serializers.DateTimeField()
    people = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ['id','table','booking_date_time_start', 'booking_date_time_end', 'people']
        extra_kwargs = {'id': {'required': True}}
        ordering = ('id',)

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id','name', 'description', 'opening_time','closing_time']
        extra_kwargs = {'name': {'required': False}}
        ordering = ('id',)

    def __str__(self):
        return self.name + "(" + self.id + ")"


class TableSerializer(serializers.ModelSerializer):
    #restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    #size = serializers.IntegerField()

    class Meta:
        model = Table
        fields = ['id','restaurant', 'size']
        #extra_kwargs = {'size': {'required': False}}
        #ordering = ('id',)

    def __str__(self):
        return self.size + "(" + self.id + ")"