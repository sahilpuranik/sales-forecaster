from marshmallow import Schema, fields

class CleanRequestSchema(Schema):
    file = fields.Raw(required=True, metadata={"description": "CSV file to clean"})

class CleanResponseSchema(Schema):
    success = fields.Boolean(required=True)
    data = fields.List(fields.Dict(), required=True)
    message = fields.String(required=True)
    quality_issues = fields.List(fields.String())
    data_insights = fields.Dict()
    pattern_insights = fields.Dict()

class ForecastRequestSchema(Schema):
    data = fields.List(fields.Dict(), required=True, metadata={"description": "Cleaned data for forecasting"})
    model = fields.String(metadata={"description": "Model to use (auto, linear, prophet)"})
    periods = fields.Integer(metadata={"description": "Number of periods to forecast"})

class ForecastResponseSchema(Schema):
    success = fields.Boolean(required=True)
    forecast = fields.List(fields.Dict(), required=True)
    message = fields.String(required=True)
    insights = fields.Dict()
    warning = fields.String()