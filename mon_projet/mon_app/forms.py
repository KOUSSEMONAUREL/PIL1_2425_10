from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import RideOffer
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'role', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
class RideOfferForm(forms.ModelForm):
    class Meta:
        model = RideOffer
        fields = ['departure', 'arrival', 'departure_time', 'seats_available']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
from django import forms
from .models import CustomUser

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'address',
            'departure_time', 'return_time', 'available_seats', 'photo'
        ]
from .models import PrivateMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2}),
        }
from django import forms
from .models import Offre

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['depart', 'arrivee', 'date_depart', 'vehicule', 'places_disponibles']
        widgets = {
            'date_depart': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'Choisir la date et l’heure de départ'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }
    def __init__(self, *args, **kwargs):
        super(OffreForm, self).__init__(*args, **kwargs)
        self.fields['date_depart'].input_formats = ['%Y-%m-%dT%H:%M']      


from django import forms
from .models import PrivateMessage

class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre message...'})
        }
from .models import PrivateMessage

class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
