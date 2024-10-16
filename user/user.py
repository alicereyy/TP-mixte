# REST API
from flask import Flask, render_template, request, jsonify, make_response
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

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)

PORT = 3005
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
   
# Returns all the booked movies of a user 
@app.route("/users/<userid>", methods = ['GET'])
def get_booking_for_userid(userid):
   for user in users:
      if str(user["id"]) == str(userid):
         with grpc.insecure_channel('localhost:3004') as channel:
            stub = booking_pb2_grpc.BookingStub(channel)
            request = booking_pb2.UserId(id=userid)
            response = stub.GetBookingsForUser(request)
            user_bookings = []
            try : 
               for booking in response:
                  for date_movie in booking.dates:
                     user_bookings.append({
                           'date': date_movie.date,
                           'movies': list(date_movie.movies)
                     })
               if user_bookings != [] : 
                  res=make_response(jsonify(user_bookings), 200)
                  return res 
               else :
                  return make_response(jsonify({"error": "This user does not have any bookings"}), 404)
            except grpc.RpcError as e:
               return make_response(jsonify({"error": "Call to booking server failed"}), 508)
            
   return(make_response(jsonify({"error": "This user does not exist in the users database"}), 400))

# Returns the booked movies of a user on the chosen date 
@app.route("/users/<userid>/<date>", methods = ['GET'])
def get_booking_by_date_user(userid, date):
   for user in users:
      if str(user["id"]) == str(userid):
         with grpc.insecure_channel('localhost:3004') as channel:
            stub = booking_pb2_grpc.BookingStub(channel)
            request = booking_pb2.UserId(id=userid)
            try:
               response = stub.GetBookingsForUser(request)
               for booking in response:
                  for date_movie in booking.dates:
                     if str(date_movie.date) == str(date):
                        return make_response(jsonify({
                           'date': date_movie.date,
                           'movies': list(date_movie.movies)
                     }), 200)
               return make_response(jsonify({"error": "There are no bookings on this date for this user"}), 409)
            except grpc.RpcError as e:
                  return make_response(jsonify({"error": "Call to booking server failed"}), 508)
   return make_response(jsonify({"error": "This user does not exist in the users database"}), 400)

def getMovieInfo(movieid) :
   #variables = {"id": movieid}
    
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
      'http://127.0.0.1:3001/graphql',
      json={'query': query}  # Send the query
   )
   
   #print(f'HHHHHH {response}')  # just for debugging
   
   if response.status_code == 200:
      return response.json()['data']['movie_with_id']
   else:
      return None

@app.route("/users/movie_info/<userid>", methods=['GET'])
def get_movies_info_for_user_bookings(userid):
   
   with grpc.insecure_channel('localhost:3004') as channel:
      stub = booking_pb2_grpc.BookingStub(channel)
      request = booking_pb2.UserId(id=userid)
   
   #if not user_bookings[0]:
   #   return make_response(jsonify({"error": "This user does not have any bookings"}), 404)
      try:
         user_bookings= stub.GetBookingsForUser(request)
         movies_infos = []
      
         for user_booking in user_bookings:
            for date_movie in user_booking.dates:
               booking_info = {
                     'date': date_movie.date,  
                     'movies': []
               }
               movies_ids = date_movie.movies

               for movieid in movies_ids:
                  movie_info = getMovieInfo(movieid)
                  if movie_info:
                     booking_info['movies'].append(movie_info)

                  #else:
                     #return make_response(jsonify({"error": f"Movie with ID {movieid} does not exist in the movies database"}), 404)

               movies_infos.append(booking_info)
               
         if movies_infos == [] :
            return make_response(jsonify({"error": "This user does not have any bookings"}), 404)
         return make_response(jsonify(movies_infos), 200)

      except grpc.RpcError as e:
         return make_response(jsonify({"error": "Call to booking server failed"}), 508)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
