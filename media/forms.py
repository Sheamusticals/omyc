
from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phoneNumber', 'message']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']

class BookingForm(forms.ModelForm):
    PACKAGES =[
        ('Medium', 'Medium'),
        ('Full', 'Full'),
        ('Rental', 'Rental'),
    ]
    CHOICE_OPTIONS = [
        ('live_stream', 'Live Stream'),
        ('Videography/Photography', 'Videography/Photography'),
         ('Event Planning', 'Event Planning'),
         ('Graphic Designing', 'Graphic Designing'),
        ('Gadget Rental', 'Gadget Rental'),
        ('MC', 'MC')
    ]
    packages = forms.ChoiceField(choices=PACKAGES, widget=forms.Select(attrs={'class': 'form-control'}))

    service_type = forms.ChoiceField(choices=CHOICE_OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Booking
        fields = ['name', 'contact','address', 'event', 'date', 'time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'event': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'service_type': forms.Select(choices=Booking.SERVICE_TYPE_CHOICES, attrs={'class': 'form-control'}),
        }
class RadioForm(forms.ModelForm):
    class Meta:
        model = Radio_Comment
        fields = ['content']