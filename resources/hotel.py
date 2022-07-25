from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hotels(Resource):
    def get(self):
        return {'hotels': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument('name', type=str, required=True, help="The field 'name' cannot be left blank.")
    arguments.add_argument('rank', type=float, required=True, help="The field 'rank' cannot be left blank.")
    arguments.add_argument('daily')
    arguments.add_argument('city')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 #Not found alert

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #Bad Request

        data = Hotel.arguments.parse_args()
        hotel = HotelModel(hotel_id, **data)
        hotel.save_hotel()
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurrred trying to save hotel.'}, 500 #Internal Server Error
        return hotel.json()
        

    def put(self, hotel_id):

        data = Hotel.arguments.parse_args()
        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            hotel_found.update_hotel(**data)
            hotel_found.save_hotel()
            return hotel_found.json(), 200 #Ok alert
        hotel = HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurrred trying to save hotel.'}, 500 #Internal Server Error
        return hotel.json(), 201 #Created alert

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurrred trying to delete hotel.'}, 500 #Internal Server Error
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404 #Not Found