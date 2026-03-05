from marshmallow import fields, validate
from app.extensions import ma
from app.models.school import School
from app.models.canteen import Canteen
from app.models.category import Category
from app.models.product import Product
from app.models.combo import Combo, ComboItem
from app.models.product_price_log import ProductPriceLog

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

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        load_instance = True

    code = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    short_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    stock = fields.Integer(load_default=0)
    cost_price = fields.Float(required=True)
    sell_price = fields.Float(required=True)
    status = fields.Boolean(load_default=True)

class ComboItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ComboItem
        include_fk = True
        load_instance = True

    quantity = fields.Integer(required=True, validate=validate.Range(min=1))

class ComboSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Combo
        include_fk = True
        load_instance = True

    code = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    short_name = fields.String(allow_none=True, validate=validate.Length(max=50))
    price_type = fields.String(validate=validate.OneOf(["auto_sum", "custom"]), load_default="auto_sum")
    custom_price = fields.Float(allow_none=True)
    image_url = fields.String(allow_none=True)
    status = fields.Boolean(load_default=True)
    
    items = fields.List(fields.Nested(ComboItemSchema), dump_only=True)
    total_price = fields.Method("get_total_price", dump_only=True)

    def get_total_price(self, obj):
        return obj.calculate_total_price()

class ProductPriceLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductPriceLog
        include_fk = True
        load_instance = True

from app.models.wallet import Wallet, WalletLimit

class WalletLimitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WalletLimit
        include_fk = True
        load_instance = True
        
class WalletSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wallet
        include_fk = True
        load_instance = True
        
    student_can_recharge = fields.Boolean(load_default=True)
    limits = fields.List(fields.Nested(WalletLimitSchema), dump_only=True)
