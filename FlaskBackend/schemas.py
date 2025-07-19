from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from werkzeug.datastructures import FileStorage
import pandas as pd

# ── Schemas ────────────────────────────────────────────────────────────────
from schemas import CleanRequestSchema, CleanResponseSchema

# ── DataScience Import ─────────────────────────────────────────────────────
from App.preprocess import clean_csv

# ── Blueprint Setup ────────────────────────────────────────────────────────
blp = Blueprint(
    "cleaning",
    __name__,
    url_prefix="/",
    description="CSV cleaning endpoint",
)


@blp.route("/clean", methods=["POST"])
class CleanResource(MethodView):
    """POST /clean – Accepts a raw CSV file, cleans it, and returns preview"""

    @blp.arguments(CleanRequestSchema, location="files")
    @blp.response(200, CleanResponseSchema(many=True))
    def post(self, args):
        # 1. Extract file from validated args
        file = args.get("file")
        if file is None:
            abort(400, message="No file uploaded. Attach it using 'file' field.")

        # 2. Basic file extension check
        if not file.filename.endswith(".csv"):
            abort(400, message="Only .csv files are supported.")

        # 3. Clean the uploaded CSV
        try:
            df = clean_csv(file)  # Returns cleaned DataFrame with 'ds' and 'y'
        except Exception:
            abort(400, message="Could not process file. Ensure it’s a valid CSV.")

        # 4. Return first few rows for preview
        return df.head().to_dict("records")