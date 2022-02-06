from django.test import TestCase
from datetime import datetime, timedelta
import pytz
from .factories import RestaurantFactory, TableFactory, BookingFactory
from restaurants import booking


class ModelsTest(TestCase):
    def setUp(self):
        self.restaurant_1 = RestaurantFactory.create(opening_time=12, closing_time=24)
        self.restaurant_1_table_1 = TableFactory.create(restaurant=self.restaurant_1, size=2)
        self.restaurant_1_table_2 = TableFactory.create(restaurant=self.restaurant_1, size=2)
        self.restaurant_1_table_3 = TableFactory.create(restaurant=self.restaurant_1, size=4)
        self.restaurant_1_table_4 = TableFactory.create(restaurant=self.restaurant_1, size=6)
        self.restaurant_1_table_5 = TableFactory.create(restaurant=self.restaurant_1, size=6)
        self.restaurant_1_table_6 = TableFactory.create(restaurant=self.restaurant_1, size=6)

        booking_date_time_start = datetime(2022, 2, 3, 19, 0, tzinfo=pytz.UTC)
        minutes_slot = 90
        delta = timedelta(seconds=60*minutes_slot)
        booking_date_time_end = booking_date_time_start + delta

        self.booking_1 = BookingFactory.create(
            table=self.restaurant_1_table_3,
            people=4,
            booking_date_time_start=booking_date_time_start,
            booking_date_time_end=booking_date_time_end)

    def test_get_first_table_available(self):
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2022, 2, 3, 20, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(table.id, self.restaurant_1_table_1.id)

    def test_get_first_table_available_unavailable_1(self):
        # The setup already books the 4 people table from 19:00 to 20:30 so this will get next table available of size 6.
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2022, 2, 3, 19, 30, tzinfo=pytz.UTC),
            people=4)
        self.assertEqual(table.id, self.restaurant_1_table_4.id)

    def test_get_first_table_available_unavailable_2(self):
        # We dont have that much seating capacity
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2022, 2, 3, 20, 10, tzinfo=pytz.UTC),
            people=8)
        self.assertEqual(table, None)

    def test_get_first_table_available_unavailable_3(self):
        # The setup already books the 4 people table from 19:00 to 20:30
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2020, 2, 3, 20, 20, tzinfo=pytz.UTC),
            people=4,
            minutes_slot=300)
        self.assertEqual(table, None)

    def test_unavailable_tables_1_hour_before_closing(self):
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2022, 2, 3, 23, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(table, None)

    def test_unavailable_tables_1_hour_before_opening(self):
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2022, 2, 3, 11, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(table, None)

    def test_book_first_available_table(self):
        booking_response = booking.book_restaurant_table(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2022, 2, 3, 20, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(booking_response['table'], self.restaurant_1_table_1.id)

    def test_get_expected_diners(self):
        booking_date_time_start = datetime(2015, 2, 14, 19, 0, tzinfo=pytz.UTC)
        minutes_slot = 90
        delta = timedelta(seconds=60*minutes_slot)
        booking_date_time_end = booking_date_time_start + delta

        self.booking_2 = BookingFactory.create(
            table=self.restaurant_1_table_1,
            people=2,
            booking_date_time_start=booking_date_time_start,
            booking_date_time_end=booking_date_time_end)
        diners = booking.get_expected_diners(self.restaurant_1,
            datetime(2022, 2, 3, tzinfo=pytz.UTC))
        self.assertEqual(diners, 4)

    def test_book_table_for_2_hours(self):
        booking_response = booking.book_restaurant_table(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2022, 2, 4, 21, 0, tzinfo=pytz.UTC),
            people=4,
            minutes_slot=120)
        self.assertEqual(booking_response['table'], self.restaurant_1_table_3.id)
