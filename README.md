# Ressources

- Pour accéder à la documentation du projet, rendez-vous sur [le wiki](https://gitlab.centralesupelec.fr/2014legerm/paul-emploi/wikis/Installation)
- Pour tester directement la version de production, rendez-vous à l'addresse [https://germoon.nebulae.co/](https://germoon.nebulae.co/#/)
- Pour accéder directement à l'API, rendez-vous à l'addresse [https://germoon.nebulae.co/api/](https://germoon.nebulae.co/api/)

# Procédure de mise en place de l'environnement de développement

## Liste des dépendances

Pour que le projet puisse fonctionner correctement, il est nécessaire d'avoir installé les dépendances suivantes :
- Python 3.6+ : https://www.python.org/
- NodeJS 8.9+ et npm 5.5+ : https://nodejs.org/
- PostreSQL 9.6+ : https://www.postgresql.fr/

## Installation

### 1. Cloner le projet :

Pour commencer il faut cloner le projet :

```sh
git clone https://gitlab.centralesupelec.fr/2014legerm/paul-emploi.git
cd paul-emploi
```

### 2. Setup le projet VueJS :

Pour configurer correctement le client il faut d'abord installer de manière globale Vue et Vue-cli

```sh
npm install --global vue
npm install --global vue-cli
```

Il faut ensuite initialiser le projet :

```sh
cd pierre-client
npm install
```

Au niveau de la configuration du frontend, il faut juste vérifier que la variable `Vue.http.options.root` ait bien l'adresse du back sur lequel on souhaite se connecter. Si l'on souhaite rester en local, il faut alors assigner la variable comme suit dans le fichier pierre-client/src/router/index.js :

```js
Vue.http.options.root = 'http://localhost:8000/'
```

### 3. Setup la base de données

#### Configuration classique de la base de données

Notre projet Django est configuré par défaut avec une base de données postgreSQL tournant en localhost sur le port 5432. La configuration suivante devrait suffire pour un démarrage rapide du projet :

- utilisateur : paul
- mot de passe : paulpaul
- nom de la base de données : paul_emploi_db

#### Utilisation de Docker

Notre projet comporte un docker-compose file permettant d'utiliser un container pour instancier la base de données. Pour cela, il suffit de se placer à la racine du projet et de lancer la commande :

```sh
docker-compose up
```

### 4. Setup le projet Django

Pour configurer le projet Django, il faut d'abord setup un environnement virtuel. Si [virtualenv](https://virtualenv.pypa.io/en/stable/) n'est pas installé :

```sh
pip install virtualenv
```

Il faut ensuite créer l'environnement virtuel dans le projet jacques_serveur :

```sh
cd jacques_serveur
virtualenv env -p "your_python_path"
```

Il faut ensuite activer l'environnement virtuel. Sous Linux :

```sh
source ./env/bin/activate
```

Et sous Windows :

```sh
./env/Scripts/activate
```

Pour installer les requirements :

```sh
pip install -r requirements.txt
```

Nous allons maintenant utiliser les commandes de Django pour que la base données puisse accueillir notre projet. Pour cela il faut faire la première migration à l'aide des deux commandes suivantes :

```sh
./manage.py makemigrations
./manage.py migrate
```

Une fois la migration terminée, il est possible de remplir la base de données avec quelques offres en utilisant la commande personnalisée :

```sh
./manage.py populatedb
```

## Faire tourner les différents serveurs

### 1. Serveur frontend

Pour faire tourner le serveur en mode développement :

```sh
cd pierre-client
npm run dev
```

### 2. Serveur backend

Pour faire tourner le serveur Django :

```sh
cd jacques_serveur
python manage.py runserver
```