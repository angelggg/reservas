from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
from django.urls import reverse

from book.room.helpers import validate_type_range_availabilty, get_total_price
from book.room.models import Book, Contact, ROOM_CHOICES
from book.room.forms import ContactForm, BookForm


def check_availability_view(request):
    """
    Ajax call to check availability on the selected date
    """
    results = dict()
    room_choices = [choice for choice in ROOM_CHOICES if choice[0] >= int(request.GET['guests'])]
    for type in room_choices:
        start = datetime.strptime(request.GET.get('start'), '%Y-%m-%d')
        end = datetime.strptime(request.GET.get('end'), '%Y-%m-%d')
        total_price = get_total_price(check_in_date=start, check_out_date=end, room_type=type[0])
        availability = validate_type_range_availabilty(check_in_date=start, check_out_date=end, room_type=type[0])
        results[type[1]] = {'available': availability, "total_price": total_price}
    return JsonResponse(results)


def room_home_view(request):
    """
    returns params for the home
    """

    start_date = datetime.today() + relativedelta(days=+1)
    end_date = start_date + relativedelta(years=+1)
    reservations = Book.objects.all().order_by('check_in_date')
    params = {'min_date': start_date.strftime('%Y-%m-%d'),
              'max_date': end_date.strftime('%Y-%m-%d'),
              'reservations': reservations
              }
    return render(request, 'home.html', params)


def book_form_view(request):
    """
    Open the booking form with selected params
    """
    params = request.GET
    type = Book.get_room_type_dict()[params['type']]
    params = {'start_date': params.get('start'),
              'end_date': params.get('end'),
              'guests': params.get('guests'),
              'type': type}
    return render(request, 'book-form.html', params)


def do_book_view(request):
    """
    Do the post request to effectively book a room
    """
    post = request.POST
    check_in_date = datetime.strptime(post.get('start'), '%Y-%m-%d')
    check_out_date = datetime.strptime(post.get('end'), '%Y-%m-%d')
    room_type = int(post.get('room-type'))
    if check_out_date <= check_in_date:
        print("VALE")
        return render(request, 'home.html',{'error': 'Wrong dates'})

    if not validate_type_range_availabilty(check_in_date=check_in_date,
                                           check_out_date=check_out_date,
                                           room_type=room_type):
        return render(request, 'home.html',{'error': 'No availability for these dates'})

    # Validate contact
    contact_data = {'name': post.get('name'), 'email': post.get('email'), 'phone': post.get('phone')}
    if not ContactForm(contact_data).is_valid():
        return render(request, 'home.html', {'error': 'Contact data provided not valid'})
    total_price = get_total_price(check_in_date=check_in_date, check_out_date=check_out_date, room_type=room_type)

    reservation_data = {'check_in_date': check_in_date, 'check_out_date': check_out_date,
                        'total_price': total_price, 'room_type': room_type,
                        'guests_number': post.get('guests')}

    if not BookForm(reservation_data).is_valid():
        return render(request, 'home.html', {'error': 'Reservation data provided not valid'})

    contact = Contact.objects.create(**contact_data)
    reservation_data = reservation_data | {'contact': contact}
    book = Book(**reservation_data)
    book.save()

    return render(request, 'home.html', {'booked': True,
                                         'check_in': book.check_in_date})
