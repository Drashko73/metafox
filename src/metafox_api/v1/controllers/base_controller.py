from metafox_shared.dal.idatastore import IDataStore

class BaseController:
    
    def __init__(self, data_store: IDataStore) -> None:
        self.data_store = data_store