# API_HydroNex

API REST pour la gestion de dispositifs de surveillance hydrologique avec système d'alertes et chatbot intelligent.

## 🚀 Fonctionnalités

- **Gestion des dispositifs** : Création, modification et suivi des capteurs hydrologiques
- **Collecte de données** : Stockage et récupération des données de température, salinité, pH, turbidité
- **Système d'alertes** : Notifications automatiques par email en cas de valeurs critiques
- **Newsletter** : Gestion des abonnements et envoi d'emails
- **Chatbot IA** : Assistant intelligent utilisant Google AI
- **Authentification JWT** : Sécurisation des endpoints
- **Documentation Swagger** : API auto-documentée

## 📋 Prérequis

- Python 3.11.8
- PostgreSQL ou MySQL
- Git

## 🛠️ Installation

### 1. Cloner le repository

```bash
git clone <url-du-repository>
cd API_HydroNex
```

### 2. Créer un environnement virtuel

```bash
# Créer l'environnement virtuel
python -m venv env

# Activer l'environnement virtuel
# Sur Linux/Mac :
source env/bin/activate
# Sur Windows :
# env\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement

1. **Créer le fichier de configuration** :
   ```bash
   # Copier le fichier d'exemple
   cp app/commons/const/const/env.example app/commons/const/const/.env
   ```

2. **Modifier le fichier `.env`** avec vos configurations :
   ```bash
   # Éditer le fichier .env
   nano app/commons/const/const/.env
   ```

   **Variables obligatoires à configurer :**
   ```env
   # Base de données (PostgreSQL recommandé)
   DATABASE_URL=postgresql://username:password@localhost:5432/hydronex_db
   
   # Clés secrètes (générer des clés sécurisées)
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   
   # Configuration SMTP (pour les emails d'alerte)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   
   # Google AI API (pour le chatbot)
   GOOGLE_API_KEY=your-google-api-key-here
   ```

### 5. Configuration de la base de données

#### Option A : PostgreSQL (Recommandé)

```bash
# Installer PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Créer la base de données
sudo -u postgres psql
CREATE DATABASE hydronex_db;
CREATE USER hydronex_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hydronex_db TO hydronex_user;
\q
```

#### Option B : MySQL

```bash
# Installer MySQL
sudo apt-get install mysql-server

# Créer la base de données
mysql -u root -p
CREATE DATABASE hydronex_db;
CREATE USER 'hydronex_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON hydronex_db.* TO 'hydronex_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 6. Initialiser la base de données

```bash
# Les migrations s'exécutent automatiquement au démarrage
# Mais vous pouvez aussi les forcer :
python -c "from app import app; app.app_context().push()"
```

## 🚀 Démarrage

### Mode développement

```bash
# Activer l'environnement virtuel si pas déjà fait
source env/bin/activate

# Lancer l'application
python app/__init__.py
```

L'API sera accessible sur : `http://localhost:5000`

### Mode production

```bash
# Utiliser Gunicorn
gunicorn wsgi:app
```

## 📚 Documentation de l'API

Une fois l'application démarrée, accédez à la documentation Swagger :

- **URL** : `http://localhost:5000/swagger`
- **Interface interactive** pour tester les endpoints

## 🔧 Endpoints principaux

### Authentification
- `POST /auth/login` - Connexion utilisateur
- `POST /auth/register` - Inscription utilisateur

### Dispositifs
- `GET /dispositifs` - Liste des dispositifs
- `POST /dispositifs` - Créer un dispositif
- `GET /dispositifs/<id>` - Détails d'un dispositif
- `PUT /dispositifs/<id>` - Modifier un dispositif
- `DELETE /dispositifs/<id>` - Supprimer un dispositif

### Données
- `POST /donnees` - Créer des données de capteur
- `GET /donnees/temps-reel` - Données en temps réel
- `GET /donnees/historique` - Historique des données

### Alertes
- `GET /alertes` - Liste des alertes
- `POST /alertes` - Créer une alerte

### Newsletter
- `POST /newsletter/subscribe` - S'abonner
- `POST /newsletter/unsubscribe` - Se désabonner

### Chatbot
- `POST /chatbot/chat` - Interagir avec le chatbot IA

## 🔐 Sécurité

- **JWT** : Authentification par tokens
- **CORS** : Configuration des origines autorisées
- **Validation** : Vérification des données d'entrée
- **Logging** : Traçabilité des actions

## 📧 Configuration SMTP

Pour les emails d'alerte, configurez un compte Gmail :

1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application
3. Utiliser ce mot de passe dans `SMTP_PASSWORD`

## 🤖 Configuration Google AI

1. Aller sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créer une clé API
3. Ajouter la clé dans `GOOGLE_API_KEY`

## 🐳 Déploiement

### Sur Render

Le projet est configuré pour un déploiement automatique sur Render :

1. Connecter votre repository GitHub à Render
2. Les variables d'environnement seront configurées automatiquement
3. Le déploiement se fait via le fichier `render.yaml`

### Variables d'environnement de production

```env
DATABASE_URL=postgresql://...
SECRET_KEY=...
JWT_SECRET_KEY=...
SMTP_SERVER=...
SMTP_PORT=...
SMTP_USERNAME=...
SMTP_PASSWORD=...
GOOGLE_API_KEY=...
```

## 🧪 Tests

```bash
# Lancer les tests (si configurés)
python -m pytest

# Ou lancer l'application en mode test
FLASK_ENV=testing python app/__init__.py
```

## 📁 Structure du projet

```
API_HydroNex/
├── app/
│   ├── adaptater/          # Couche d'adaptation
│   ├── commons/            # Utilitaires communs
│   │   └── const/const/    # Configuration (.env)
│   ├── controllers/        # Contrôleurs
│   ├── core/              # Configuration principale
│   ├── data/              # Modèles de données
│   ├── routes/            # Définition des routes
│   ├── services/          # Services métier
│   └── uses_cases/        # Cas d'usage
├── migrations/            # Migrations de base de données
├── requirements.txt       # Dépendances Python
├── wsgi.py               # Point d'entrée WSGI
└── render.yaml           # Configuration Render
```

## 🐛 Dépannage

### Erreur de connexion à la base de données
- Vérifier que PostgreSQL/MySQL est démarré
- Vérifier les paramètres de connexion dans `.env`
- Vérifier que la base de données existe

### Erreur d'importation
- Vérifier que l'environnement virtuel est activé
- Réinstaller les dépendances : `pip install -r requirements.txt`

### Erreur de migration
- Supprimer le dossier `migrations/` et relancer l'application
- Les tables seront recréées automatiquement

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Consulter la documentation Swagger
- Vérifier les logs de l'application

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
