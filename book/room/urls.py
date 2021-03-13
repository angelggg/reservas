from django.urls import path
from book.room import views

urlpatterns = [
    path('', views.room_home_view, name='room-home'),
    path(r'check-availability', views.check_availability_view, name='check-availability'),
    path(r'book-form', views.book_form_view, name='book-form'),
    path(r'do-book', views.do_book_view, name="do-book")
]