from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': ' ',
            'id': 'username_email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': ' ',
            'id': 'password'
        })
    )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': ' ',
            'id': 'email'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': ' ',
                'id': 'username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input',
            'placeholder': ' ',
            'id': 'username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input',
            'placeholder': ' ',
            'id': 'reg_password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input',
            'placeholder': ' ',
            'id': 'conreg_password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['adresse_depart', 'horaire_debut', 'horaire_fin', 'nombre_places', 'photo_profil', 'type_utilisateur', 'telephone']
        widgets = {
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
            'photo_profil': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'type_utilisateur': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+229 XX XX XX XX'
            })
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            })
        }