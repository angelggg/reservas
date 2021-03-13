from datetime import timedelta

from book.room.models import Book, ROOM_AVAILABILITY, ROOM_PRICES

def validate_type_range_availabilty(check_in_date, check_out_date, room_type):
    """
    return the smallest amount of free rooms in the given range for the type
    """
    min = ROOM_AVAILABILITY[room_type]
    while check_in_date < check_out_date:
        check_in_date = check_in_date + timedelta(days=1)
        reservations_done = Book.check_books_per_type_date(date=check_in_date, type=room_type)
        if ROOM_AVAILABILITY[room_type] <= reservations_done:
            return False
        if min > (ROOM_AVAILABILITY[room_type] - reservations_done):
            min = ROOM_AVAILABILITY[room_type] - reservations_done
    return min

def get_total_price(check_in_date, check_out_date, room_type):
    """
    returns the total price days * price
    """
    delta = check_out_date - check_in_date
    total_price = delta.days * ROOM_PRICES[room_type]
    return total_price