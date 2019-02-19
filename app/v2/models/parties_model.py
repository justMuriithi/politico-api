from app.v2.util.validate import generate_id, exists, validate_ints
from app.v2.util.validate import validate_strings
from .base_model import BaseModel


class Party(BaseModel):
    """ model for political party """

    def __init__(self, name=None, hqaddress=None, id=None):
        super().__init__('Party', 'parties')

        self.name = name
        self.hqaddress = hqaddress
        self.id = id

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "hqaddress": self.hqaddress
        }

    def save(self):
        """save party to db  """

        data = super().save('name, hqaddress', self.name, self.hqaddress)

        self.id = data.get('id')
        return data

    def from_json(self, json):
        self.__init__(json['name'], json['hqaddress'])
        self.id = json['id']
        return self

    def edit(self, new_name):
        """ Edit party name """
        self.name = new_name
        return super().edit('name', new_name, self.id)

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.name, self.hqaddress):
            self.error_message = "Integer types are not allowed for some fields"
            self.error_code = 400
            return False

        if self.find_by('name', self.name):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 409
            return False

        return super().validate_object()
