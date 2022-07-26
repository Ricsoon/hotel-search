from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(city=None, rank_min=0,rank_max=5, daily_min=0, daily_max=10000, limit=50, offset=0, **data):
    if city:
        return {
            "rank_min": rank_min,
            "rank_max": rank_max,
            "daily_min": daily_min,
            "daily_max": daily_max,
            "city": city,
            "limit": limit,
            "offset": offset
        }
    return {
            "rank_min": rank_min,
            "rank_max": rank_max,
            "daily_min": daily_min,
            "daily_max": daily_max,
            "limit": limit,
            "offset": offset
        }

# Path example -> /hotels?city=Recife&rank_min=4&daily_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('rank_min', type=float)
path_params.add_argument('rank_max', type=float)
path_params.add_argument('daily_min', type=float)
path_params.add_argument('daily_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hotels(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        data = path_params.parse_args()
        valid_data = {key: data[key] for key in data if data[key] is not None}
        parameters = normalize_path_params(**valid_data,)

        if not parameters.get('city'):
            query = "SELECT * FROM hotels WHERE (rank >= ? and rank <= ?) and (daily >= ? and daily <= ?) LIMIT ? OFFSET ?"
            tupla = tuple([parameters[key] for key in parameters])
            result = cursor.execute(query, tupla)
        else:
            query = "SELECT * FROM hotels WHERE (rank >= ? and rank <= ?) and (daily >= ? and daily <= ?) and city = ? LIMIT ? OFFSET ?"
            tupla = tuple([parameters[key] for key in parameters])
            result = cursor.execute(query, tupla)
        
        hotels = []
        for row in result:
            hotels.append({
            'hotel_id': row[0],
            'name': row[1],
            'rank': row[2],
            'daily': row[3],
            'city': row[4]
            })
        return {'hotels': [hotels]}

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

    @jwt_required()
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
        
    @jwt_required()
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

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurrred trying to delete hotel.'}, 500 #Internal Server Error
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404 #Not Found