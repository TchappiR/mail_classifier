# 🎫 Assistant IA de Classification de Tickets Support

Ce projet automatise le traitement du support client de niveau 1. Il lit les e-mails entrants via l'API Gmail, utilise l'IA (via l'API Groq) pour en extraire la catégorie, l'urgence et une synthèse, puis enregistre automatiquement ces informations structurées dans un tableau Google Sheets.

## 📂 Structure du projet

* **`main.py`** : Le script principal (chef d'orchestre) qui lance le processus.
* **`mail_reader.py`** : Module chargé de se connecter à Gmail et de récupérer les e-mails non lus.
* **`classifier_agent.py`** : Module qui envoie le contenu de l'e-mail à l'IA Groq pour obtenir un JSON structuré.
* **`sheet_writer.py`** : Module qui ajoute une nouvelle ligne dans votre Google Sheet.
* **`config.py`** : Fichier de configuration des paramètres de l'IA (modèle, température).
* **`prompt.txt`** : Les instructions exactes (le "cerveau") données à l'IA.
* **`pyproject.toml` / `poetry.lock`** : Fichiers de gestion des dépendances via Poetry.
* **`.python-version`** : Version de Python recommandée pour ce projet.

---

## 🛠️ Prérequis

1.  **Python** (la version est spécifiée dans le fichier `.python-version`).
2.  **Poetry** installé sur votre machine pour gérer l'environnement virtuel et les dépendances.
3.  Un compte **Google Cloud Console** (pour les accès Gmail et Sheets).
4.  Un compte **Groq** pour obtenir une clé API.

---

## ⚙️ Installation

1.  Clonez ce dépôt sur votre machine locale :
    ```bash
    git clone https://github.com/TchappiR/classification_mails.git
    ```
2.  Installez les dépendances du projet grâce à Poetry :
    ```bash
    poetry install
    ```

---

## 🔑 Configuration des APIs (Étape cruciale)

Ce projet nécessite trois éléments de configuration secrets pour fonctionner. **Ne publiez jamais ces fichiers sur GitHub (ajoutez-les à votre `.gitignore`).**

### 1. Clé API Groq (IA)
1. Créez un compte sur la [console Groq](https://console.groq.com/) et générez une clé API.
2. Créez un fichier nommé `.env` à la racine du projet et ajoutez-y la clé ainsi que l'URL de votre Google Sheet :
    ```env
    GROQ_API_KEY=votre_cle_api_groq_ici
    SHEET_URL=https://docs.google.com/spreadsheets/d/VOTRE_ID_DE_FICHIER/edit
    ```

### 2. Google Sheets API (`credentials_sheet.json`)
Ce fichier permet au script d'écrire dans votre tableau Google Sheets.
1. Allez sur la [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un projet et activez les API **Google Sheets API** et **Google Drive API**.
3. Allez dans **Identifiants > Créer des identifiants > Compte de service**.
4. Générez une clé au format **JSON**, téléchargez-la, renommez-la en `credentials_sheet.json` et placez-la à la racine du projet.
5. ⚠️ **Important :** Ouvrez ce fichier JSON, copiez l'adresse e-mail `client_email` qui s'y trouve. Allez sur votre Google Sheet, cliquez sur "Partager" et donnez les droits d'**Éditeur** à cette adresse.

### 3. Gmail API (`credentials_gmail.json`)
Ce fichier permet au script de lire vos e-mails.
1. Sur le même projet Google Cloud, activez l'API **Gmail API**.
2. Configurez l'**Écran de consentement OAuth** (choisissez "Externe" et ajoutez votre adresse e-mail en tant qu'utilisateur test).
3. Allez dans **Identifiants > Créer des identifiants > ID client OAuth**.
4. Choisissez le type **"Application de bureau"**.
5. Téléchargez le fichier JSON généré, renommez-le en `credentials_gmail.json` et placez-le à la racine du projet.

---

## 🚀 Utilisation

Une fois la configuration terminée, vous pouvez lancer l'assistant avec Poetry :

```bash
poetry run python main.py
```
