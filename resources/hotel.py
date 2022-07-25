from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hotels = [
    {
        'hotel_id': 'alpha',
        'name': 'Alpha Hotel',
        'rank': 4.3,
        'daily': 450.23,
        'city': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'name': 'Bravo Hotel',
        'rank': 3.8,
        'daily': 250.60,
        'city': 'São Paulo'
    },
    {
        'hotel_id': 'charlie',
        'name': 'Charlie Hotel',
        'rank': 5.0,
        'daily': 500.50,
        'city': 'Recife'
    }
]

class Hotels(Resource):
    def get(self):
        return {'hotels': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument('name')
    arguments.add_argument('rank')
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
        return hotel.json()
        

    def put(self, hotel_id):

        data = Hotel.arguments.parse_args()
        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            hotel_found.update_hotel(**data)
            hotel_found.save_hotel()
            return hotel_found.json(), 200 #Ok alert
        hotel = HotelModel(hotel_id, **data)
        hotel.save_hotel()
        return hotel.json(), 201 #Created alert

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404 #Not Found