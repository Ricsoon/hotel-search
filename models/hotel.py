from sqlalchemy import ForeignKey
from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hotels'

    hotel_id = banco.Column(banco.String, primary_key=True)
    name = banco.Column(banco.String(80))
    rank = banco.Column(banco.Float(precision=1))
    daily = banco.Column(banco.Float(precision=2))
    city = banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer, ForeignKey('sites.site_id'))

    def __init__(self, hotel_id, name, rank, daily, city, site_id):
        self.hotel_id = hotel_id
        self.name = name
        self.rank = rank
        self.daily = daily
        self.city = city
        self.site_id = site_id
    
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'rank': self.rank,
            'daily': self.daily,
            'city': self.city,
            'site_id': self.site_id
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, name, rank, daily, city):
        self.name = name
        self.rank = rank
        self.daily = daily
        self.city = city

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()