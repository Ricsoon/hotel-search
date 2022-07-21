class HotelModel:
    def __init__(self, hotel_id, name, rank, daily, city):
        self.hotel_id = hotel_id
        self.name = name
        self.rank = rank
        self.daily = daily
        self.city = city
    
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'rank': self.rank,
            'daily': self.daily,
            'city': self.city
        }