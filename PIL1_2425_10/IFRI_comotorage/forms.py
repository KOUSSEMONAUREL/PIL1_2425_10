from django import forms
from .models import RideOffer, UserProfile
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.utils import timezone
from datetime import time

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'input', 
            'placeholder': ''
        })
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'input', 
            'placeholder': ''
        })
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'input', 
            'placeholder': ''
        })
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe', 
        widget=forms.PasswordInput(attrs={
            'class': 'input', 
            'placeholder': ''
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur existe déjà.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Changé de "password" à "password1"
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'input', 
            'placeholder': ''
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input', 
            'placeholder': ''
        })
    )
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@exemple.com'
            }),
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo_profil', 'type_utilisateur', 'adresse_depart', 
                 'horaire_debut', 'horaire_fin', 'nombre_places', 'telephone']
        widgets = {
            'photo_profil': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'type_utilisateur': forms.Select(attrs={
                'class': 'form-control'
            }),
            'adresse_depart': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre adresse de départ habituelle'
            }),
            'horaire_debut': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horaire_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'nombre_places': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '8'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+229 XX XX XX XX'
            }),
        }
        labels = {
            'photo_profil': 'Photo de profil',
            'type_utilisateur': 'Type d\'utilisateur',
            'adresse_depart': 'Adresse de départ habituelle',
            'horaire_debut': 'Horaire de début habituel',
            'horaire_fin': 'Horaire de fin habituel',
            'nombre_places': 'Nombre de places disponibles',
            'telephone': 'Téléphone',
        }

class RideOfferForm(forms.ModelForm):
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        initial=timezone.now().date(),
        required=True
    )
    
    departure_latitude = forms.FloatField(
        required=False, 
        widget=forms.HiddenInput()
    )
    departure_longitude = forms.FloatField(
        required=False, 
        widget=forms.HiddenInput()
    )
    arrival_latitude = forms.FloatField(
        required=False, 
        widget=forms.HiddenInput()
    )
    arrival_longitude = forms.FloatField(
        required=False, 
        widget=forms.HiddenInput()
    )

    class Meta:
        model = RideOffer
        fields = [
            'departure_location', 'departure_latitude', 'departure_longitude', # Ajout des champs de coordonnées
            'arrival_location', 'arrival_latitude', 'arrival_longitude',       # Ajout des champs de coordonnées
            'departure_date', 'departure_time', 'available_seats'
        ]
        widgets = {
            'departure_location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Adresse de départ'}),
            'arrival_location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Adresse d\'arrivée'}),
            'departure_time': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'available_seats': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Nombre de places disponibles'}),
        }


RideOfferFormSet = inlineformset_factory(
    User, RideOffer, form=RideOfferForm,
    fields=[
        'departure_location', 'departure_latitude', 'departure_longitude',
        'arrival_location', 'arrival_latitude', 'arrival_longitude',
        'departure_date', 'departure_time', 'available_seats'
    ],
    extra=1,
    can_delete=True
)


class RechercheForm(forms.Form):
    search_location = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Rechercher un lieu'})
    )
    search_latitude = forms.FloatField(
        required=False, 
        widget=forms.HiddenInput(attrs={'id': 'id_search_latitude'})
    )
    search_longitude = forms.FloatField(
        required=False, 
        widget=forms.HiddenInput(attrs={'id': 'id_search_longitude'})
    )
    
class RechercheAvanceeForm(forms.Form):
    depart = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Adresse de départ'})
    )
    arrivee = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Adresse d\'arrivée'})
    )
    depart_lat = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_depart_lat'}))
    depart_lon = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_depart_lon'}))
    arrivee_lat = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_arrivee_lat'}))
    arrivee_lon = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_arrivee_lon'}))