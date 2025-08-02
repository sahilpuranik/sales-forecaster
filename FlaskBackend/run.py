#Entry point for Flask
from flask import Flask, jsonify
from flask_smorest import Api
from flask_cors import CORS

from cleaning_routes import blp as cleaning_blp
from forecast_routes import blp as forecast_blp


def create_app() -> Flask:
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

    app.config.update(
        SECRET_KEY="dev-only-change-me",
        API_TITLE="Sales Forecasting API",
        API_VERSION="1.0",
        OPENAPI_VERSION="3.0.2",
        OPENAPI_URL_PREFIX="/",          # -> /openapi.json
        OPENAPI_SWAGGER_UI_PATH="/docs", # -> /docs
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    )

    api = Api(app)
    api.register_blueprint(cleaning_blp)
    api.register_blueprint(forecast_blp)
    
    # Add a simple health check endpoint
    @app.route("/")
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "Sales Forecaster API is running",
            "endpoints": {
                "docs": "/docs",
                "clean": "/clean",
                "forecast": "/forecast"
            }
        })
    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)