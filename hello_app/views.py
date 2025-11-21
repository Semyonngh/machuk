from django.shortcuts import render, redirect
from .models import Concert, Ticket, TicketOrder
from django.utils import timezone

def concerts_list(request):
    concerts = Concert.objects.all().select_related('artist', 'venue').prefetch_related('ticket_set')
    return render(request, 'all.html', {'concerts': concerts})

def concert_detail(request, concert_id):
    concert = Concert.objects.get(id=concert_id)
    tickets = Ticket.objects.filter(concert=concert).select_related('category_id')
    return render(request, 'concert_detail.html', {
        'concert': concert,
        'tickets': tickets
    })

def buy_ticket(request, concert_id):
    if request.method == 'POST':
        concert = Concert.objects.get(id=concert_id)
        ticket_id = request.POST.get('ticket_id')
        
        try:
            ticket = Ticket.objects.get(id=ticket_id, concert=concert)
            
            
            if ticket.quantity < int(request.POST['quantity']):
                return render(request, 'error.html', {
                    'message': 'Недостаточно билетов в наличии'
                })
            
            
            order = TicketOrder(
                concert=concert,
                ticket=ticket,
                customer_name=request.POST['name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                ticket_type=request.POST['ticket_type'],
                quantity=int(request.POST['quantity']),
            )
            order.save()
            
            
            ticket.quantity -= order.quantity
            ticket.save()
            
            return redirect('order_success', order_id=order.id)
            
        except Ticket.DoesNotExist:
            return render(request, 'error.html', {
                'message': 'Билет не найден'
            })
    
    return redirect('concert_detail', concert_id=concert_id)

def order_success(request, order_id):
    order = TicketOrder.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})

def online(request):
    return concerts_list(request)
