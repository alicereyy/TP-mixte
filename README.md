# Application micro-services avec API mixtes (REST, GraphQL et gRPC)

## Description de l'application
Cette application est une application jouet et peu réaliste pour gérer les films et les réservations d’utilisateurs dans un cinéma. Elle est composée de 4 micro-services.

### Movie (API GraphQL)
C'est le micro-service responsable de la gestion des films du cinéma. Il contient et gère une petite base de données json contenant la liste des films disponibles avec quelques informations sur les films.

### Times (API gRPC)
C'est le micro-service responsable des jours de passage des films dans le cinéma. Il contient et gère une petite base de données json contenant la liste des dates avec l’ensemble des films disponibles à cette date.

### Booking (API gRPC)
C'est le micro-service responsable de la réservation des films par les utilisateurs. Il contient et gère une petite base de données json contenant une entrée par utilisateurs avec la liste des dates et films réservés. Booking fait appel à Times pour connaître et vérifier que les créneaux réservés existent bien puisqu’il ne connait pas lui même les créneaux des films.

### User (API REST)
C'est le micro-service qui sert de point d’entrée à tout utilisateur et qui permet ensuite de récupérer des informations sur les films, sur les créneaux disponibles et de réserver. Il contient et gère une petite base de données json avec la liste des utilisateurs. User fait appel à Booking et Movie pour respectivement permettre aux utilisateurs de réserver un film ou d’obtenir des informations sur les films.


## Fonctionnalités 
Le point d'entrée utilisateur est le micro-service User. Les fonctionnalités disponibles dans le service User sont:
- get all users (no parameter)
- get booked movies for a user (parameter in url: user id)
- get booked movies for a user with movie information (parameter in url: user id)
- get booked movies of a user on the chosen date (parameters in url: user id, date)
- add a booking to a user (parameter in url: user id) (json request: date, movie id)
- delete a booking for a user (parameter in url: user id) (json request: date, movie id)
- get available movies on date, with movie information (parameter in url: date)
- get dates from movie title (json request: movie title)


## Lancer l'application
- télécharger le projet
- activer l'environnement virtuel (ou installer les requirements avec 'pip install -r requirements.txt')
- avec Python, run en parallèle les fichiers user.py, booking.py, showtimes.py et movie.py qui se trouvent respectivement dans les dossiers user, booking, showtime et movie

Il est possible de tester l'application avec Postman ou équivalent. Le point d'entrée utilisateur est le micro-service User. Pour tester ses fonctionnalités, faire des requètes http avec l'url du serveur local et les routes spécifiées dans le fichier user.py.
