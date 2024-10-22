import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

# Showtime is a server to booking 
class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
    def GetSchedule(self, request, context):
        for schedule in self.db:
            yield showtime_pb2.Schedule(date=schedule['date'], movies=schedule['movies'])
            
    # This function will be used in user to let the user know the available movies to watch on a chosen date 
    def GetMoviesOnDate(self, request, context):
        for schedule in self.db:
            if schedule['date'] == request.date:
                print("Movies found on this date!")
                return showtime_pb2.Schedule(date=schedule['date'], movies=schedule['movies'])
        print("No movies on this date")
        return showtime_pb2.Schedule(date=request.date, movies=[])
    # This function will be used in user to let the user know the available dates to watch a movie 
    def GetDatesForMovie(self, request, context):
        dates = []
        for schedule in self.db:
            if request.id in schedule['movies']:
                dates.append(schedule['date'])
        return showtime_pb2.Dates(dates=dates)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
