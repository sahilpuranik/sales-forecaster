"""
Blueprint handling the /clean endpoint for CSV file uploads and cleaning.
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.datastructures import FileStorage
import pandas as pd

# Schemas
from schemas import CleanRequestSchema, CleanResponseSchema

# Data cleaning logic
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from App.preprocess import clean_data

# Blueprint
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
            # Read the uploaded file into a DataFrame first
            df = pd.read_csv(file)
            # Then clean it using our function
            cleaned_df = clean_data(df)
        except Exception as e:
            abort(400, message=f"Could not process file: {str(e)}")

        # 4. Return first few rows for preview
        return cleaned_df.head().to_dict("records")