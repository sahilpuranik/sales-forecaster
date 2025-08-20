from flask import Flask
from flask_cors import CORS
from cleaning_routes import cleaning_bp
from forecast_routes import forecast_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(cleaning_bp, url_prefix="/clean")
    app.register_blueprint(forecast_bp, url_prefix="/forecast")
    
    # Health check endpoint
    @app.route("/health")
    def health_check():
        return {"status": "healthy", "message": "Sales Forecasting API is running"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)