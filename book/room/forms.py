from django.forms import ModelForm
from book.room.models import Contact, Book, ROOM_CHOICES


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "phone", "email"]

    def clean(self):
        super(ContactForm, self).clean()
        name = self.cleaned_data.get('name')
        phone = self.cleaned_data.get('phone')
        email = self.cleaned_data.get('email')
        if not all([len(s) > 5 for s in (name, phone, email)]):
            self._errors["missing_fields"] = "Missing fields"
        return self.cleaned_data


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["check_in_date", "check_out_date", "total_price", "guests_number", "room_type"]

    def clean(self):
        super(BookForm, self).clean()
        check_in_date = self.cleaned_data.get('check_out_date')
        check_out_date = self.cleaned_data.get('check_out_date')
        total_price = self.cleaned_data.get('total_price')
        guests_number = self.cleaned_data.get('guests_number')
        room_type = self.cleaned_data.get('room_type')

        if room_type not in [x[0] for x in ROOM_CHOICES]:
            self._errors["Faulty room type"] = "Faulty room type"

        if total_price <= 0:
            self._errors["Free"] = "Free reservation"

        if guests_number > room_type:
            self._errors["room_to_small"] = "Not suitable room"

        return self.cleaned_data
