from app.v2.util.validate import validate_strings
from .base_model import BaseModel


class Office(BaseModel):
    """ model for political office """

    def __init__(self, name=None, category=None, id=None):
        super().__init__('Office', 'offices')

        self.name = name
        self.category = category
        self.id = id

    def save(self):
        """save office to db """

        data = super().save('name, category', self.name, self.category)

        self.id = data.get('id')
        return data

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }

    def from_json(self, json):
        self.__init__(json['name'], json['category'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.name, self.category):
            self.error_message = (
                "Integer types are not allowed for some"
                " fields")
            self.error_code = 422
            return False

        if self.find_by('name', self.name):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 409
            return False

        return super().validate_object()
