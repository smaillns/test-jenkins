"""Schemas."""

from marshmallow import fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from installation_requests.models import InstallationRequest


class InstallationRequestSchema(Schema):
    """InstallationRequestSchema class."""

    id = fields.Int(required=True)
    created_at = fields.Date()
    updated_at = fields.Date()
    user_id = fields.Int(required=True)
    type = fields.Str(required=True)
    status = fields.Str(required=True)
    budget = fields.Decimal(as_string=True)
    equipment_type = fields.Str(required=True)
    equipment_brand = fields.Str()
    equipment_model = fields.Str()
    comment = fields.Str()


class CreateInstallationRequestSchema(SQLAlchemyAutoSchema):
    """CreateInstallationRequestSchema."""

    class Meta:
        """Meta."""

        model = InstallationRequest
        load_instance = True

    equipment_type = fields.Str(validate=validate.OneOf(["SOLAR", "DEMOTIC", "INVERTER", "OTHER"]))
