from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q

from .models import Concert, Artist, Venue, Ticket, TicketOrder, Category
from .serializers import (
    ConcertSerializer, ArtistSerializer, VenueSerializer,
    TicketSerializer, TicketOrderSerializer, CategorySerializer
)


class ConcertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Concert.objects.all().select_related('artist', 'venue').prefetch_related('ticket_set__category_id')
    serializer_class = ConcertSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(venue__city__iexact=city)
        
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(artist__genre__iexact=genre)
        
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(ticket__price__lte=max_price).distinct()
        
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(
                Q(artist__name__icontains=q) |
                Q(venue__city__icontains=q) |
                Q(venue__name__icontains=q) |
                Q(description__icontains=q)
            )
        
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        return self.list(request)


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(['GET'])
def filter_options(request):
    cities = sorted(set(Concert.objects.values_list('venue__city', flat=True)))
    genres = sorted(set(Artist.objects.values_list('genre', flat=True).exclude(genre='')))
    return Response({'cities': cities, 'genres': genres})


@api_view(['POST'])
def buy_ticket(request, concert_id):
    try:
        concert = Concert.objects.get(id=concert_id)
    except Concert.DoesNotExist:
        return Response({'error': 'Концерт не найден'}, status=404)

    ticket_id = request.data.get('ticket_id')
    quantity = int(request.data.get('quantity', 1))

    try:
        ticket = Ticket.objects.get(id=ticket_id, concert=concert)
    except Ticket.DoesNotExist:
        return Response({'error': 'Билет не найден'}, status=404)

    if ticket.quantity < quantity:
        return Response({'error': 'Недостаточно билетов'}, status=400)

    order = TicketOrder.objects.create(
        concert=concert,
        ticket=ticket,
        customer_name=request.data.get('name'),
        email=request.data.get('email'),
        phone=request.data.get('phone'),
        ticket_type=request.data.get('ticket_type'),
        quantity=quantity,
    )

    ticket.quantity -= quantity
    ticket.save()

    serializer = TicketOrderSerializer(order)
    return Response(serializer.data, status=201)


@api_view(['GET'])
def order_detail(request, order_id):
    try:
        order = TicketOrder.objects.get(id=order_id)
    except TicketOrder.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=404)
    serializer = TicketOrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET'])
def orders_by_email(request, email):
    orders = TicketOrder.objects.filter(email=email).order_by('-order_date')
    serializer = TicketOrderSerializer(orders, many=True)
    return Response(serializer.data)