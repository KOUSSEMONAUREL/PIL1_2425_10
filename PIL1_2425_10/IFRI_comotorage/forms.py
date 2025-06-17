from django import forms
from .models import RideOffer, UserProfile
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.utils import timezone
from datetime import time

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nom d\'utilisateur'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirmer le mot de passe'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nom d\'utilisateur ou Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Mot de passe'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['adresse_depart', 'horaire_debut', 'horaire_fin', 'nombre_places', 'photo_profil', 'type_utilisateur', 'telephone']
        widgets = {
            'adresse_depart': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Adresse de départ préférée'}),
            'horaire_debut': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'horaire_fin': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'nombre_places': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Nombre de places'}),
            'photo_profil': forms.ClearableFileInput(attrs={'class': 'input'}),
            'type_utilisateur': forms.Select(attrs={'class': 'input'}),
            'telephone': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Numéro de téléphone'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
        }

class RideOfferForm(forms.ModelForm):
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        initial=timezone.now().date(),
        required=True
    )
    # NOUVEAUX CHAMPS CACHÉS POUR LA PUBLICATION
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

# Mise à jour du formset pour inclure les nouveaux champs de coordonnées
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
