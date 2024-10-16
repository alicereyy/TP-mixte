import threading
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc

import showtime_pb2
import showtime_pb2_grpc
import json
from multiprocessing import Process
import time

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    def GetAllBookings(self, request,context):
        for booking in self.db:
            yield booking_pb2.BookingInfo(userid=booking['userid'], dates=[booking_pb2.DateMovies(date=date['date'], movies = date['movies']) for date in booking['dates']])
        
    def GetBookingsForUser(self, request, context):
        response = booking_pb2.BookingsForUser()
        
        for booking in self.db:
            if booking['userid'] == request.id:
                print("user found")
                yield booking_pb2.BookingsForUser(dates=[booking_pb2.DateMovies(date=date['date'],movies = date['movies']) for date in booking['dates']])
            print("No bookings for this user")

    def AddBookingForUser(self, request, context):
        with grpc.insecure_channel ('localhost:3003') as channel:
            
            showtime_stub = showtime_pb2_grpc.ShowtimeStub(channel)
            
            showtime_response = showtime_stub.GetMoviesOnDate(showtime_pb2.Date(date=request.dates[0].date))
            
            
            existing_movies = [movie for movie in request.dates[0].movies if movie in showtime_response.movies]
            print (existing_movies)
            
            if not existing_movies:
                return booking_pb2.ResponseMessage(message="There are no movies on this date.")
            
        for booking in self.db:
            if booking['userid'] == request.userid:
                # if the user exists, check if the date exists
                for date_movie in booking['dates']:
                    if date_movie['date'] == request.dates[0].date:
                        #print (f'HHHHHHHHHHHHH {date_movie['date']}')
                        # add the new movies to the corresponding movie date
                        date_movie['movies'].extend(request.dates[0].movies)
                        return booking_pb2.ResponseMessage(message="Movies added to existing date for this user")
                
                # If the date does not exist, add the whole booking
                booking['dates'].append({
                    'date': request.dates[0].date,
                    'movies': request.dates[0].movies
                })
                return booking_pb2.ResponseMessage(message="Booking added for this user.")
        return booking_pb2.ResponseMessage(message="Booking already exists for this user")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3004')
    server.start()
    server.wait_for_termination()
'''
def run():
    time.sleep(2)
    with grpc.insecure_channel('localhost:3002') as booking_channel:
        booking_stub = booking_pb2_grpc.BookingStub(booking_channel)
        booking_request = booking_pb2.BookingInfo(
            userid= "chris_rivers",
            dates=[
                booking_pb2.DateMovies(
                    date="20151130",
                    movies=["a8034f44-aee4-44cf-b32c-74cf452aaaae"]
                )
            ]
        )
        #print(booking_request)
        # Apply the AddBookingForUser method 
        response = booking_stub.AddBookingForUser(booking_request)
        print("Response: ", response.message)
'''

def run():
    # Delay to ensure server is up
    time.sleep(2)
    
    with grpc.insecure_channel('localhost:3004') as booking_channel:
        booking_stub = booking_pb2_grpc.BookingStub(booking_channel)
        booking_request = booking_pb2.BookingInfo(
            userid="chris_rivers",
            dates=[
                booking_pb2.DateMovies(
                    date="20151130",
                    movies=["a8034f44-aee4-44cf-b32c-74cf452aaaae"]
                )
            ]
        )
       
        print("Booking Request: ", booking_request)
        # Apply the AddBookingForUser method 
        response = booking_stub.AddBookingForUser(booking_request)
        print("-------------- AddBookingForUser --------------")
        print("Response: ", response.message)
        
if __name__ == '__main__':
    # Start the server in a separate process
    server_process = Process(target=serve)
    server_process.start()

    # Run the client
    run()

    # Stop the server process after test
    server_process.terminate()
    server_process.join()
    
'''               
if __name__ == '__main__':
    server_thread = threading.Thread(target=serve)
    server_thread.start()
    serve()
    run()
''' 
    