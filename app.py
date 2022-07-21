from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
        return {'hotels': hotels}

api.add_resource(Hotels, '/hotels')

if __name__ == '__main__':
    app.run(debug=True)