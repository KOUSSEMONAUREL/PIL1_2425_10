from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, RideOffer
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.utils import timezone

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nom d\'utilisateur ou Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Mot de passe'}))

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
    # Ajoutez un initial pour la date de départ pour qu'elle s'affiche par défaut avec la date du jour
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        initial=timezone.now().date(), # Définit la date du jour comme valeur initiale
        required=True # Le champ est requis
    )

    class Meta:
        model = RideOffer
        fields = ['departure_location', 'arrival_location', 'departure_date', 'departure_time', 'available_seats']
        widgets = {
            'departure_location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Adresse de départ'}),
            'arrival_location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Adresse d\'arrivée'}),
            # 'departure_date' est déjà défini ci-dessus avec son initial
            'departure_time': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'available_seats': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Nombre de places disponibles'}),
        }

RideOfferFormSet = inlineformset_factory(
    User, RideOffer, form=RideOfferForm,
    fields=['departure_location', 'arrival_location', 'departure_date', 'departure_time', 'available_seats'],
    extra=1,
    can_delete=True
)