from app.v2.models.offices_model import Office
from app.v2.models.parties_model import Party


class Database:
    """ The database model """
    PARTIES = 'parties'
    OFFICES = 'offices'

    def __init__(self):
        self.tables = {
            self.PARTIES: Party.parties,
            self.OFFICES: Office.offices
        }

    def get_table(self, table_name):
        return self.tables[table_name]

    def clear(self, table_name=None):
        # clears the entire database or single table
        if table_name:
            self.tables[table_name] = []
        else:
            for key in self.tables.items:
                self.tables[key] = []