from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found.'}, 404 #Not Found

    def post(self, url):
        if SiteModel.find_site(url):
            return {"message": "The site '{}' already exists.".format(url)}, 400 #Bad Request
        site = SiteModel(url)
        try:
            site.save_site(url)
        except: 
            return {'message': 'An internal error ocurred trying to create a new site.'}
        return site.json()

    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted.'}
        return {'message': 'Site not found.'}, 404 #Not Found
