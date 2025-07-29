from marshmallow import Schema, fields, ValidationError
from flask_smorest import Blueprint

# Schema for file upload requests
class CleanRequestSchema(Schema):
    file = fields.Raw(required=True, description="CSV file to clean")

# Schema for cleaned data response
class CleanResponseSchema(Schema):
    ds = fields.Date(required=True, description="Date")
    y = fields.Float(required=True, description="Sales amount")

# Schema for forecast requests
class ForecastRequestSchema(Schema):
    data = fields.List(fields.Dict(), required=True, description="Cleaned data array")

# Schema for forecast response
class ForecastResponseSchema(Schema):
    forecast = fields.List(fields.Dict(), required=True, description="Forecast results")
    low_confidence = fields.Boolean(required=True, description="Whether forecast has low confidence")