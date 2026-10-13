from rest_framework import serializers
from .models import Category, Artist, Venue, Concert, Ticket, TicketOrder


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'description', 'image', 'genre']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'city', 'address', 'capacity']


class TicketSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='category_id', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'price', 'quantity', 'category']


class ConcertSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    tickets = TicketSerializer(source='ticket_set', many=True, read_only=True)
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Concert
        fields = [
            'id', 'artist', 'venue', 'start_time', 'end_time',
            'description', 'tickets', 'min_price'
        ]

    def get_min_price(self, obj):
        return obj.get_min_price()


class TicketOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketOrder
        fields = '__all__'
        read_only_fields = ['order_number', 'order_date', 'total_price']