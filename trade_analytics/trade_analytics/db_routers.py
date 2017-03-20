
import random

class StockPriceRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'dataapp':
            return 'stockpricedata'

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'dataapp':
            return 'stockpricedata'

        return None
        # database = getattr(model, "_DATABASE", None)
        # return database


    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'dataapp' or \
           obj2._meta.app_label == 'dataapp':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db=='stockpricedata':
            if app_label == 'dataapp':
                return True
            else:
                return False            

        if app_label == 'dataapp':
            
            if db == 'stockpricedata':
                return True
            else:
                return False
            # return db == 'stockpricedata'

        return None
