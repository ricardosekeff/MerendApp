from marshmallow import fields, validate
from app.extensions import ma
from app.models.school import School
from app.models.canteen import Canteen
from app.models.category import Category

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

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True
        load_instance = True

    code = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    short_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    safety_stock = fields.Integer(load_default=0)
    image_url = fields.String(allow_none=True)
    status = fields.Boolean(load_default=True)
