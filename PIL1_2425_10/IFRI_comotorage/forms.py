from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        # Configuration du champ username
        self.fields['username'].widget.attrs.update({
            'class': 'input',
            'placeholder': ' ',
            'id': 'username'
        })
        # Configuration du champ password1 (mot de passe)
        self.fields['password1'].widget.attrs.update({
            'class': 'input',
            'placeholder': ' ',
            'id': 'reg_password'
        })
        # Configuration du champ password2 (confirmation)
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