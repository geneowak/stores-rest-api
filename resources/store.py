from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': "Store not found."}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A Store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except :
            return {'message': 'There was an error creating the store.'}, 500
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except :
                return {'message': 'There was an error deleting the store.'}, 500
        else:
            return {'message': 'Store was not found.'}

        return {'message': 'Store was successfully removed.'}            


class StoreList(Resource):
    
    def get(self):
        try:
            stores = StoreModel.get_stores()
        except :
            return {'message': 'There was an error retrieving the stores.'}, 500
        
        if stores:
            return {'stores': [store.json() for store in stores]}
        else:
            return {'message': 'No stores were found.'}
