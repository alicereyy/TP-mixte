import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def write(self, bookings):
        print("trying to write")
        with open('{}/data/bookings.json'.format("."), 'w') as f:
            json.dump({"bookings": bookings}, f)

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
            showtime_response = showtime_stub.GetMoviesOnDate(showtime_pb2.Date(date=request.date))

            # if the movie is not programmed on this date
            if not request.movieid in showtime_response.movies :
                return booking_pb2.ResponseMessage(message="This movie does not exist on this date")
        
        for booking in self.db:
            if booking['userid'] == request.userid:
                # if the user exists, check if the date exists
                for date_movie in booking['dates']:
                    if date_movie['date'] == request.date:
                        if not request.movieid in date_movie['movies']:
                            # add the new movie to the corresponding movie date
                            date_movie['movies'].append(request.movieid)
                            self.write(self.db)
                            return booking_pb2.ResponseMessage(message="Booking added for this user")
                        else:
                            return booking_pb2.ResponseMessage(message="Booking already exists for this user")
                # If the date does not exist, add the whole booking
                booking['dates'].append({
                    'date': request.date,
                    'movies': [request.movieid]
                })
                self.write(self.db)
                return booking_pb2.ResponseMessage(message="Booking added for this user")       

        # if the user is not found   
        return booking_pb2.ResponseMessage(message="This user does not exist in the database")       

    def DeleteBookingForUser(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.userid: # find the user
                for date_movie in booking['dates']: 
                    if date_movie['date'] == request.date: # find the date
                        try:
                            date_movie['movies'].remove(request.movieid)

                            # # if no more bookings on this date for this user
                            # if date_movie['movies'] == []:
                            #     booking['date'].remove(
                            #         {
                            #             "date": request.date,
                            #             "movies": []
                            #         }
                            #     )
                            self.write(self.db)
                            return booking_pb2.ResponseMessage(message="Booking deleted for this user")
                        except:
                            return booking_pb2.ResponseMessage(message="Booking does not exist for this user")
                # if the date is not found in the user bookings
                return booking_pb2.ResponseMessage(message="Booking does not exist for this user")
        
        # if the user is not found
        return booking_pb2.ResponseMessage(message="This user does not exist in the database")    
    
    def GetMoviesOnDate(self, request, context):
        with grpc.insecure_channel ('localhost:3003') as channel:    
            showtime_stub = showtime_pb2_grpc.ShowtimeStub(channel)
            showtime_response = showtime_stub.GetMoviesOnDate(showtime_pb2.Date(date=request.date))
            return booking_pb2.DateMovies(date=showtime_response.date, movies=showtime_response.movies)
            
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3004')
    server.start()
    server.wait_for_termination()

        
if __name__ == '__main__':
    serve()


    