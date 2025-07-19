"""
Blueprint handling the /forecast endpoint.
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
import pandas as pd

# Schemas
from schemas import ForecastRequestSchema, ForecastResponseSchema

# Forecasting logic
from App.forecast import run_forecast  # adjust path if needed

# Blueprint
blp = Blueprint(
    "forecast",
    __name__,
    url_prefix="/",
    description="Forecasting endpoint",
)


@blp.route("/forecast", methods=["POST"])
class ForecastResource(MethodView):
    """POST /forecast — receive cleaned data, return predictions"""

    @blp.arguments(ForecastRequestSchema)
    @blp.response(200, ForecastResponseSchema)
    def post(self, parsed_json):
        data = parsed_json.get("data", [])
        if not data:
            abort(400, message="Request body must include 'data' list.")

        df = pd.DataFrame(data)
        expected_cols = {"ds", "y"}
        if set(df.columns) != expected_cols:
            abort(400, message=f"Columns must be {expected_cols}.")

        try:
            forecast_df = run_forecast(df)
        except Exception as exc:
            abort(500, message=str(exc))

        return {
            "forecast": forecast_df.to_dict(orient="records"),
            "low_confidence": bool(
                forecast_df.get("low_confidence", pd.Series(dtype=bool)).any()
            ),
        }