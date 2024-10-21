# REST API
import time
from flask import Flask, render_template, request, jsonify, make_response, Response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
#import movie_pb2
#import movie_pb2_grpc


app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods = ['GET'])
def get_json():
   res = make_response(jsonify(users), 200)
   return res

# Function to write in the users json file (used in update last active)
def write(users):
   print("trying to write")
   with open('{}/data/users.json'.format("."), 'w') as f:
      json.dump({"users": users}, f)
            
# A separate function to be reused not to access the booking server each time
def get_user_bookings(userid):
   
   update_last_active(userid)
   
   with grpc.insecure_channel('localhost:3004') as channel:
      stub = booking_pb2_grpc.BookingStub(channel)
      request = booking_pb2.UserId(id=userid)
      try:
         response = stub.GetBookingsForUser(request)
         user_bookings = []
         for booking in response:
               for date_movie in booking.dates:
                  user_bookings.append({
                     'date': date_movie.date,
                     'movies': list(date_movie.movies)
                  })
         return user_bookings
      except grpc.RpcError as e:
         return None

# Returns all the booked movies of a user 
@app.route("/users/<userid>", methods = ['GET'])
def get_booking_for_userid(userid):
   update_last_active(userid)
   for user in users:
      if str(user["id"]) == str(userid):
         user_bookings = get_user_bookings(userid)
         if user_bookings is not None:
               if user_bookings:
                  return make_response(jsonify(user_bookings), 200)
               else:
                  return make_response(jsonify({"error": "This user does not have any bookings"}), 404)
         else:
               return make_response(jsonify({"error": "Call to booking server failed"}), 508)

   return make_response(jsonify({"error": "This user does not exist in the users database"}), 400)


# Returns the booked movies of a user on the chosen date 
@app.route("/users/<userid>/<date>", methods = ['GET'])
def get_booking_by_date_user(userid, date):
   
   update_last_active(userid)
   
   for user in users:
      if str(user["id"]) == str(userid):
         user_bookings = get_user_bookings(userid)
         if user_bookings is not None:
               for booking in user_bookings:
                  if str(booking['date']) == str(date):
                     return make_response(jsonify(booking), 200)
               return make_response(jsonify({"error": "There are no bookings on this date for this user"}), 409)
         else:
               return make_response(jsonify({"error": "Call to booking server failed"}), 508)

   return make_response(jsonify({"error": "This user does not exist in the users database"}), 400)


def getMovieInfo(movieid) :
   
    
   query = '''
    {
      movie_with_id(_id: "{movieid}") {
        id
        title
        director
        rating
        actors {
          id
          firstname
          lastname
          birthyear
        }
      }
    }
    '''.replace("{movieid}", movieid)
    
   response = requests.post(
      #'http://10.6.73.83:3001/graphql',
      'http://127.0.0.1:3001/graphql',
      json={'query': query}  # Send the query
   )
   
   #print(f'HHHHHH {response}')  # just for debugging
   
   if response.status_code == 200:
      return response.json()['data']['movie_with_id']
   else:
      return None

#Returns the movie information of each movie booked for a user 
@app.route("/users/movie_info/<userid>", methods=['GET'])
def get_movies_info_for_user_bookings(userid):
   
   update_last_active(userid)
   
   user_bookings = get_user_bookings(userid)
   if user_bookings is not None:
      movies_infos = []
      for user_booking in user_bookings:
         booking_info = {
               'date': user_booking['date'],  
               'movies': []
         }
         movies_ids = user_booking['movies']

         for movieid in movies_ids:
               movie_info = getMovieInfo(movieid)
               if movie_info:
                  booking_info['movies'].append(movie_info)
         movies_infos.append(booking_info)
               
      if movies_infos:
         return make_response(jsonify(movies_infos), 200)
      return make_response(jsonify({"error": "This user does not have any bookings"}), 404)

   return make_response(jsonify({"error": "Call to booking server failed"}), 508)


#Add a booking to a user
@app.route("/users/add_booking/<userid>", methods=['POST'])
def add_booking_for_user(userid):
   update_last_active(userid)
   # request : date and movieid
   req = request.get_json()

   with grpc.insecure_channel('localhost:3004') as channel:
      stub = booking_pb2_grpc.BookingStub(channel)
      booking_request = booking_pb2.BookingUser(userid=userid, date=req["date"], movieid=req["movieid"])
      try:
         response = stub.AddBookingForUser(booking_request)
         if response.message == "Booking added for this user":
               return make_response(jsonify({"message":response.message}), 200)
         else:
               return make_response(jsonify({"message":response.message}), 400)

      except grpc.RpcError as e:
         return make_response(jsonify({"error": "Call to booking server failed"}), 508)


#Delete a booking for a user
@app.route("/users/delete_booking/<userid>", methods=['DELETE'])
def delete_booking_for_user(userid):
   update_last_active(userid)
   # request : date and movieid
   req = request.get_json()

   with grpc.insecure_channel('localhost:3004') as channel:
      stub = booking_pb2_grpc.BookingStub(channel)
      booking_request = booking_pb2.BookingUser(userid=userid, date=req["date"], movieid=req["movieid"])
      try:
         response = stub.DeleteBookingForUser(booking_request)
         if response.message == "Booking deleted for this user":
               return make_response(jsonify({"message":response.message}), 200)
         else:
               return make_response(jsonify({"message":response.message}), 400)

      except grpc.RpcError as e:
         return make_response(jsonify({"error": "Call to booking server failed"}), 508)


#Get available movies on date, with movie information
@app.route("/users/movies/<date>", methods=['GET'])
def get_movies_on_date(date):
   
   with grpc.insecure_channel('localhost:3004') as channel:
      stub = booking_pb2_grpc.BookingStub(channel)
      booking_request = booking_pb2.BookingDate(date=date)
      try:
         response = stub.GetMoviesOnDate(booking_request)

         if response.movies == []: # if no movies on this date
            return make_response(jsonify({"message":"No movies on this date"}), 400)
         
         # collect all movies information on this date
         movie_info = []
         for movieid in response.movies:
            movie_info.append(getMovieInfo(movieid))
         
         date_movies = {
               "date": date,
               "movies": movie_info
         }
         return make_response(jsonify(date_movies), 200)

      except grpc.RpcError as e:
         return make_response(jsonify({"error": "Call to booking server failed"}), 508)


def get_id_with_title(title):
   query = '''
   {
     movie_with_title(_title: "{title}") {
       id
     }
   }
   '''.replace("{title}", title)

    
   response = requests.post(
      #'http://10.6.73.83:3001/graphql',
      'http://127.0.0.1:3001/graphql',
      json={'query': query}  # Send the query
   )

   if response.status_code == 200:
      return response.json()['data']['movie_with_title']
   else:
      return None

#Get the dates that can be booked for the chosen movie 
@app.route("/users/schedule/title", methods=['GET'])  
def get_dates_with_title():
   # request : movie title
   req = request.get_json()

   movie_response = get_id_with_title(req['title'])
   if not movie_response:
      return make_response(jsonify({"message": "Movie title not in database"}), 400)
       
   movieid = movie_response['id']

   with grpc.insecure_channel('localhost:3004') as channel:
      stub = booking_pb2_grpc.BookingStub(channel)
      booking_request = booking_pb2.Movie(id=movieid)

      try:
         response = stub.GetDatesForMovie(booking_request)

         if len(response.dates) == 0: # if no date were found
            return make_response(jsonify({"message":"No date for this movie"}), 400)
         
         movie_dates = {
                "movie": movieid,
                "dates": list(response.dates)
            }
         return make_response(jsonify(movie_dates), 200)
 
      except grpc.RpcError as e:
         return make_response(jsonify({"error": "Call to booking server failed"}), 508)

# A method to update the last active date for a user: the Unix time will be updated whenever the user 
# accesses one of the previous services 
def update_last_active(userid):
   current_time = int(time.time())  
   
   for user in users:  
      if user["id"] == userid:
         user["last_active"] = current_time
         write(users)  
         break
         
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
