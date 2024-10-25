# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import booking_pb2 as booking__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in booking_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class BookingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllBookings = channel.unary_stream(
                '/Booking/GetAllBookings',
                request_serializer=booking__pb2.OtherEmpty.SerializeToString,
                response_deserializer=booking__pb2.Bookings.FromString,
                _registered_method=True)
        self.GetBookingsForUser = channel.unary_stream(
                '/Booking/GetBookingsForUser',
                request_serializer=booking__pb2.UserId.SerializeToString,
                response_deserializer=booking__pb2.BookingsForUser.FromString,
                _registered_method=True)
        self.AddBookingForUser = channel.unary_unary(
                '/Booking/AddBookingForUser',
                request_serializer=booking__pb2.BookingUser.SerializeToString,
                response_deserializer=booking__pb2.ResponseMessage.FromString,
                _registered_method=True)
        self.DeleteBookingForUser = channel.unary_unary(
                '/Booking/DeleteBookingForUser',
                request_serializer=booking__pb2.BookingUser.SerializeToString,
                response_deserializer=booking__pb2.ResponseMessage.FromString,
                _registered_method=True)
        self.GetMoviesOnDate = channel.unary_unary(
                '/Booking/GetMoviesOnDate',
                request_serializer=booking__pb2.BookingDate.SerializeToString,
                response_deserializer=booking__pb2.DateMovies.FromString,
                _registered_method=True)
        self.GetDatesForMovie = channel.unary_unary(
                '/Booking/GetDatesForMovie',
                request_serializer=booking__pb2.Movie.SerializeToString,
                response_deserializer=booking__pb2.BookingDates.FromString,
                _registered_method=True)


class BookingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAllBookings(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBookingsForUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddBookingForUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteBookingForUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMoviesOnDate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatesForMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BookingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllBookings': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAllBookings,
                    request_deserializer=booking__pb2.OtherEmpty.FromString,
                    response_serializer=booking__pb2.Bookings.SerializeToString,
            ),
            'GetBookingsForUser': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBookingsForUser,
                    request_deserializer=booking__pb2.UserId.FromString,
                    response_serializer=booking__pb2.BookingsForUser.SerializeToString,
            ),
            'AddBookingForUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddBookingForUser,
                    request_deserializer=booking__pb2.BookingUser.FromString,
                    response_serializer=booking__pb2.ResponseMessage.SerializeToString,
            ),
            'DeleteBookingForUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteBookingForUser,
                    request_deserializer=booking__pb2.BookingUser.FromString,
                    response_serializer=booking__pb2.ResponseMessage.SerializeToString,
            ),
            'GetMoviesOnDate': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMoviesOnDate,
                    request_deserializer=booking__pb2.BookingDate.FromString,
                    response_serializer=booking__pb2.DateMovies.SerializeToString,
            ),
            'GetDatesForMovie': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatesForMovie,
                    request_deserializer=booking__pb2.Movie.FromString,
                    response_serializer=booking__pb2.BookingDates.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Booking', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Booking', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Booking(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAllBookings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/Booking/GetAllBookings',
            booking__pb2.OtherEmpty.SerializeToString,
            booking__pb2.Bookings.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetBookingsForUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/Booking/GetBookingsForUser',
            booking__pb2.UserId.SerializeToString,
            booking__pb2.BookingsForUser.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddBookingForUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Booking/AddBookingForUser',
            booking__pb2.BookingUser.SerializeToString,
            booking__pb2.ResponseMessage.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteBookingForUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Booking/DeleteBookingForUser',
            booking__pb2.BookingUser.SerializeToString,
            booking__pb2.ResponseMessage.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetMoviesOnDate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Booking/GetMoviesOnDate',
            booking__pb2.BookingDate.SerializeToString,
            booking__pb2.DateMovies.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetDatesForMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Booking/GetDatesForMovie',
            booking__pb2.Movie.SerializeToString,
            booking__pb2.BookingDates.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
