"""
Blueprint handling the /clean endpoint for CSV file uploads and cleaning.
"""

import pandas as pd
import io
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Blueprint, request, jsonify
from App.preprocess import clean_data, validate_data_quality, get_data_insights

cleaning_bp = Blueprint("cleaning", __name__)

def validate_file_size(file):
    """Check if file size is reasonable"""
    file.seek(0, 2)  # Go to end of file
    size = file.tell()
    file.seek(0)  # Go back to start
    
    if size > 10 * 1024 * 1024:  # 10MB limit
        return False
    return True

def validate_csv_structure(file):
    """Check if file looks like a CSV with sales data"""
    try:
        # Read first few lines to check structure
        content = file.read(1024).decode('utf-8')
        file.seek(0)
        
        lines = content.split('\n')
        if len(lines) < 2:
            return False
        
        # Check if it has comma-separated values
        first_line = lines[0]
        if ',' not in first_line:
            return False
        
        return True
    except:
        return False

@cleaning_bp.route("/", methods=["POST"])
def clean_csv():
    """Clean and validate uploaded CSV file"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "File must be a CSV"}), 400
    
    # Validate file size
    if not validate_file_size(file):
        return jsonify({"error": "File too large (max 10MB)"}), 400
    
    # Validate CSV structure
    if not validate_csv_structure(file):
        return jsonify({"error": "Invalid CSV format"}), 400
    
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        if len(df) == 0:
            return jsonify({"error": "CSV file is empty"}), 400
        
        # Clean the data
        cleaned_df = clean_data(df)
        
        # Get data quality information
        quality_info = validate_data_quality(cleaned_df)
        pattern_info = get_data_insights(cleaned_df)
        
        # Convert to list of dictionaries for JSON response
        data_list = []
        for _, row in cleaned_df.iterrows():
            data_dict = {
                'ds': row['ds'].strftime('%Y-%m-%d'),
                'y': float(row['y']),
                '_quality_issues': quality_info['issues'],
                '_data_insights': quality_info['insights'],
                '_pattern_insights': pattern_info
            }
            data_list.append(data_dict)
        
        return jsonify({
            "success": True,
            "data": data_list,
            "message": f"Successfully cleaned {len(data_list)} rows of data",
            "quality_issues": quality_info['issues'],
            "data_insights": quality_info['insights'],
            "pattern_insights": pattern_info
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500