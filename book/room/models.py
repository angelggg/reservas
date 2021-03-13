import random
from functools import lru_cache

from django.db import models
from django.db.models import Q

ROOM_CHOICES = ((1, 'Individual'),
                (2, 'Doble'),
                (3, 'Triple'),
                (4, 'Cuadruple'))

ROOM_AVAILABILITY = {
    1: 10,
    2: 5,
    3: 4,
    4: 6
}

ROOM_PRICES = {
    1: 20,
    2: 30,
    3: 40,
    4: 50
}


class Contact(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    email = models.CharField(max_length=200, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)


class Book(models.Model):
    check_in_date = models.DateField(null=False, blank=False)
    check_out_date = models.DateField(null=False, blank=False)
    guests_number = models.SmallIntegerField(null=False, blank=False)
    room_type = models.SmallIntegerField(choices=ROOM_CHOICES)
    total_price = models.FloatField(null=False, blank=False)
    room_number = models.IntegerField(null=True, blank=True)
    unique_code = models.CharField(max_length=16, unique=True, default='')
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Override save to add unique code is added
        """
        if not self.id:
            while True:
                code = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
                if not Book.objects.filter(unique_code=code).exists():
                    self.unique_code = code
                    break
        return super(Book, self).save(*args, **kwargs)

    @staticmethod
    def check_books_per_type_date(date: str, type: int) -> int:
        return Book.objects.filter(Q(Q(check_in_date__lte=date) & Q(check_out_date__gte=date)),
                                   room_type=type).count()

    @staticmethod
    @lru_cache(maxsize=1)
    def get_room_type_dict() -> dict:
        return {
            'Individual': 1,
            'Doble': 2,
            'Triple': 3,
            'Cuadruple': 4}

    @property
    @lru_cache(maxsize=4)
    def room_type_name(self) -> str:
        return {
            1: 'Individual',
            2: 'Doble',
            3: 'Triple',
            4: 'Cuadruple'}[self.room_type]
