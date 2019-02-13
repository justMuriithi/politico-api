from app.v2.util.validate import generate_id, exists, validate_ints, validate_bool
from app.v2.util.validate import validate_strings
from .base_model import BaseModel


class User(BaseModel):

    users = []

    def __init__(self, first_name=None, last_name=None, national_id=None, email=None, is_admin=False):
        super().__init__('User', self.users)

        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id
        self.email = email
        self.is_admin = is_admin

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "national_id": self.national_id,
            "email": self.email,
            "isAdmin": self.is_admin
        }

    def from_json(self, json):
        self.__init__(json['firstname'], json['lastname'], json['national_id'], json['email'], json['isAdmin'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.first_name, self.last_name, self.email):
            self.error_message = "Integer types are not allowed for some fields"
            self.error_code = 400
            return False

        if not validate_ints(self.national_id):
            self.error_message = "National ID is supposed to be an integer"
            self.error_code = 400
            return False

        if not validate_bool(self.is_admin):
            self.error_message = "isAdmin is supposed to be a boolean value"
            self.error_code = 400
            return False

        if exists('email', self.email, self.table):
            self.error_message = "A {} with that email already exists".format(self.object_name)
            self.error_code = 400
            return False

        return super().validate_object()