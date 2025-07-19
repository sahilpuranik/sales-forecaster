from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.datastructures import FileStorage
import pandas as pd

# Schemas
from schemas import CleanRequestSchema, CleanResponseSchema

# Data-science helper
from DataScience.preprocess import clean_csv  # adjust import path if needed

# Blueprint
blp = Blueprint(
    "cleaning",
    __name__,
    url_prefix="/",
    description="CSV cleaning endpoint",
)


@blp.route("/clean", methods=["POST"])
class CleanResource(MethodView):
    """POST /clean — upload CSV, return cleaned preview"""

    @blp.arguments(CleanRequestSchema, location="files")       # validate upload
    @blp.response(200, CleanResponseSchema(many=True))         # validate output
    def post(self, args):
        file: FileStorage | None = args.get("file")
        if file is None:
            abort(400, message="Missing file field 'file'.")

        if not file.filename.endswith(".csv"):
            abort(400, message="Only .csv files are supported.")

        try:
            df = clean_csv(file)  # returns DataFrame with 'ds' and 'y'
        except Exception:
            abort(400, message="Failed to read or clean CSV.")

        return df.head().to_dict(orient="records")