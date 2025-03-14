# Utilise une image officielle Python 3.12.1
FROM python:3.12.1-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement requirements.txt pour utiliser le cache Docker
COPY requirements.txt .


# Installer toutes les dépendances en une seule ligne
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier les fichiers du projet dans le conteneur
COPY . .

# Lancer le botgit comm
CMD ["python", "app.py"]
