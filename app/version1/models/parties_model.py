from app.version1.util.validate import generate_id, exists, validate_ints
from app.version1.util.validate import validate_strings
from .base_model import BaseModel


class Party(BaseModel):
    """ model for political party """

    parties = []

    def __init__(self, name=None, hqAddress=None):
        super().__init__('Party', self.parties)

        self.name = name
        self.hqAddress = hqAddress

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "hqAddress": self.hqAddress
        }

    def from_json(self, json):
        self.__init__(json['name'], json['hqAddress'])
        self.id = json['id']
        return self

    def edit(self, new_name):
        """ Edit party name """
        self.name = new_name
        for i in range(len(self.parties)):
            if self.parties[i]['id'] == self.id:
                party = self.parties[i]
                party['name'] = new_name
                self.parties[i] = party
                break

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.name, self.hqAddress):
            self.error_message = "Integer types are not allowed for this field"
            self.error_code = 400
            return False

        if exists('name', self.name, self.parties):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 400
            return False

        return super().validate_object()
