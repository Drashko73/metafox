from metafox_shared.dal.idatastore import IDataStore
from celery import Celery

class BaseController:
    
    def __init__(self, data_store: IDataStore) -> None:
        self.data_store = data_store
        self.celery = Celery()
        self.celery.config_from_object('metafox_api.celeryconfig')