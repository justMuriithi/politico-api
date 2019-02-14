from app.v2.util.validate import generate_id, exists, validate_ints
from app.v2.util.validate import validate_strings
from .base_model import BaseModel

class Vote(BaseModel):
    """ model for political vote """

    def __init__(self, created_by=None, office=None, candidate=None, id=None):
        super().__init__('Vote', 'votes')

        self.created_by = created_by
        self.office = office
        self.candidate = candidate
        self.id = id

    def save(self):
        """save vote to db """

        data = super().save(
            'createdby, office, candidate', self.created_by, self.office,
            self.candidate)

        self.id = data.get('id')
        return data

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "createdBy": self.created_by,
            "office": self.office,
            "candidate": self.candidate,
        }

    def from_json(self, json):
        self.__init__(json['createdBy'], json['office'], json['candidate'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_ints(self.created_by, self.candidate, self.office):
            self.error_message = "String types are not allowed for all fields"
            self.error_code = 422
            return False

        if self.get_one(
            "SELECT * FROM {} where createdby = '{}' and office = '{}';\
                ".format(self.table_name, self.created_by, self.office)):
            self.error_message = "You can only vote once per office"
            self.error_code = 409
            return False

        return super().validate_object()