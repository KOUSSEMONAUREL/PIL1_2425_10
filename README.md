# 🚗 IFRI_comotorage


![Covoiturage](https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Carsharing_icon.svg/1024px-Carsharing_icon.svg.png)


**Plateforme de covoiturage destinée aux étudiants de l'IFRI - Université d’Abomey-Calavi**

## 🎯 Objectif du projet

IFRI_comotorage est une application web visant à faciliter les trajets partagés entre les étudiants de l’IFRI, en mettant en relation conducteurs et passagers selon leurs trajets quotidiens domicile-campus.

Ce projet s’inscrit dans le cadre du **Projet Intégrateur 2024-2025** de la 1ère année de Licence à l’IFRI.


## 🧑‍💻 Équipe projet — Groupe PIL1_2425_[NUMÉRO_DU_GROUPE]

- **GL1** : BIDIBI Emeline-Nellie
- **IA1** : KUISSOPA-MANTE Vernon Dabawi
- **IM1** : HOUANNOU Marcos Primaël
- **SEIOT1** : ZOSSOU Crédo Fréjus
- **SI1** : ADJAGBA Océane Adégnika
- **SI1** : KOUSSEMON Godwill Aurel Sèdjro


## 🗂️ Organisation et Méthodologie

- **Outils utilisés** : Git, GitHub, Trello
- **Méthodologie** : travail collaboratif par répartition des rôles (backend, frontend, base de données, documentation)
- **Suivi** : points réguliers sur Trello et commits Git fréquents de chaque membre
- **Encadrement** : M. Armand ACCROMBESSI, Mme Maryse GAHOU, M. Ratheil HOUNDJI
  

## 🧩 Fonctionnalités principales

### 🔐 Authentification & profils

- Inscription avec rôle (conducteur ou passager)
- Connexion par e-mail ou téléphone
- Modification du profil (photo, horaires, lieu de départ, véhicule)

### 🧠 Matching intelligent

- Publication d'offres ou demandes
- Algorithme de mise en correspondance basé sur :
  - Proximité géographique (rayon de 10 km)
  - Compatibilité horaire
- Affichage des résultats avec infos essentielles

### 💬 Messagerie

- Envoi de messages texte en temps réel
- Historique des conversations
- Notifications de nouveaux messages

### 📱 Interface responsive

- Conception mobile-first
- Navigation intuitive, ergonomique et moderne


## 🛠️ Technologies utilisées

| Composant        | Technologie(s)                        |
| ---------------- | ------------------------------------- |
| Frontend         | HTML, CSS, JavaScript,                |
| Backend          | Django 5.2.3 (Python)                 |
| Temps réel      | Channels (ASGI) + Daphne + WebSockets |
| Base de données | MySQL                                 |
| Authentification | Django-Allauth, Systeme local         |
| Environnement    | Python-dotenv, Environ                |


## 🧭 Guide utilisateur

1. **Connexion / Inscription**

   - Accède à `/accounts/login/` ou `/accounts/signup/`
   - Crée un compte conducteur ou passager
2. **Accueil**

   - Informations générales sur la plateforme
3. **Recherche de trajets**

   - Menu `Rechercher` → recherche par adresse
   - Voir les détails et accéder au chat
4. **Publication d’un trajet**

   - Menu `Publier` → remplissage du formulaire
5. **Chat**

   - Bouton “Ouvrir le chat” sur une annonce
   - Discussion en temps réel avec l’autre utilisateur
6. **Profil**

   - Modification de tes infos à tout moment


## 🛠️ Déploiement local (mode développeur)

### ⚙️ Prérequis

- Python 3.10+
- MySQL
- pip + virtualenv

### 📥 Installation

```bash
git clone https://github.com/ton-repo/PIL1_2425_[NUMERO_DU_GROUPE].git
cd IFRI_comotorage/
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt


### ⚙️ Configuration

Crée un fichier `.env` :

SECRET_KEY=votre_clé_django
DEBUG=True
DB_NAME=ifri_comotorage
DB_USER=root
DB_PASSWORD=mot_de_passe
DB_HOST=localhost


### 🗃️ Base de données

```bash
mysql -u root -p < database.sql
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 🚀 Lancer le serveur

```bash
python manage.py runserver
```

Accède à l’application via [http://127.0.0.1:8000](http://127.0.0.1:8000)


## 🧱 Structure du projet

```bash

```

└── 📁PIL1_2425_10
    └── 📁IFRI_comotorage
        └── __init__.py
        └── 📁__pycache__
        └── admin.py
        └── apps.py
        └── consumers.py
        └── forms.py
        └── 📁management
            └── 📁commands
                └── __init__.py
                └── create_missing_ride_chats.py
        └── models.py
        └── routing.py
        └── 📁static
            └── 📁IFRI_comotorage
                └── 📁images
                    └── back.png
                    └── car.png
                    └── car2.png
                    └── logo_IFRI_comotorage.png
                └── LICENCES
                └── script.js
                └── script1.js
                └── script2.js
                └── script4.js
                └── styles.css
                └── styles1.css
                └── styles2.css
                └── styles3.css
        └── 📁templates
            └── 📁IFRI_comotorage
                └── Accueil.html
                └── index.html
                └── Login.html
                └── Messagerie.html
                └── pre-Messagerie.html
                └── Profil.html
                └── profile_config.html
                └── Publier.html
                └── Rechercher.html
        └── tests.py
        └── urls.py
        └── views.py
    └── 📁media
        └── 📁profile_pics
            └── image.jpg
    └── 📁PIL1_2425_10
        └── __init__.py
        └── 📁__pycache__
        └── .env
        └── asgi.py
        └── settings.py
        └── urls.py
        └── wsgi.py
    └── .gitignore
    └── manage.py
    └── requirements.txt




## 💾 Base de données

Le fichier `database.sql` contient :

- Création des tables `UserProfile`, `Trajet`, `Message`, etc.
- Contraintes d'intégrité (liens FK, clés uniques...)



## 📊 Diagrammes & Modèles

- **Modèle relationnel** : disponible dans `doc/diagramme_bd.png`
- **DFD et cas d’utilisation** : fournis dans le rapport technique



## 📚 Annexes

- Rapport HTML : `rapport/index.html`
- Documentation technique complète
- Manuel d’utilisation
- Cahier de charges initial disponible en PDF



## ✅ Respect du cahier des charges

- ✅ Utilisation exclusive de Django et MySQL
- ✅ Communication temps réel (WebSockets)
- ✅ Sécurité : authentification, données sécurisées
- ✅ Interface responsive
- ✅ Collaboration Git/GitHub complète



## 📅 Dates clés

- Démarrage : 30 mai 2025
- Design final : 6 juin 2025
- Livraison : 18 juin 2025



## 🪪 Licence

Ce projet est distribué sous une **licence libre**.
Vous pouvez l'utiliser, le modifier et le redistribuer conformément aux termes de la licence [MIT](https://opensource.org/licenses/MIT) ou équivalente.

Projet académique — IFRI / UAC 2025
Encadré par : **M. Armand ACCROMBESSI**, **Mme Maryse GAHOU**, **M. Ratheil HOUNDJI**
