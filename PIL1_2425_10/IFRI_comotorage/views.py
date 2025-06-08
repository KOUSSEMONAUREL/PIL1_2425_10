from django.shortcuts import render 

def index (request):
    return render(request, 'IFRI_comotorage/index.html')

def Accueil (request):
    return render(request, 'IFRI_comotorage/Accueil.html')

def signup (request):
    return render(request, 'IFRI_comotorage/signup.html')

def signin (request):
    return render(request, 'IFRI_comotorage/signin.html')

def Rechercher (request):
    return render(request, 'IFRI_comotorage/Rechercher.html')

def Publier (request):
    return render(request, 'IFRI_comotorage/Publier.html')

def Messagerie (request):
    return render(request, 'IFRI_comotorage/Messagerie.html')

def Profil (request):
    return render(request, 'IFRI_comotorage/Profil.html')