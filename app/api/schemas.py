from marshmallow import fields, validate
from app.extensions import ma
from app.models.school import School
from app.models.canteen import Canteen

class SchoolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = School
        include_fk = True
        load_instance = True

    name = fields.String(required=True, validate=validate.Length(min=3, max=255))
    cnpj = fields.String(required=True, validate=validate.Length(min=14, max=18))
    phone = fields.String(allow_none=True)
    address = fields.String(allow_none=True)
    city = fields.String(allow_none=True)
    state = fields.String(allow_none=True, validate=validate.Length(equal=2))
    active = fields.Boolean(load_default=True)

class CanteenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Canteen
        include_fk = True
        load_instance = True

    name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    active = fields.Boolean(load_default=True)
