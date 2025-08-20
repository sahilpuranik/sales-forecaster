# 📊 Sales Forecaster

A beginner-friendly web application that helps small businesses forecast their sales using AI. Simply upload your sales data and get instant predictions with educational insights!

## ✨ Features

- **Smart Data Cleaning**: Automatically detects and cleans date and sales columns from your CSV files
- **AI-Powered Forecasting**: Uses advanced machine learning models (Prophet and Linear Regression) to predict future sales
- **Educational Insights**: Learn about your data patterns and how AI makes predictions
- **Data Quality Validation**: Identifies potential issues in your data and provides guidance
- **Beautiful UI**: Modern, intuitive interface that guides you through each step
- **Confidence Intervals**: See prediction ranges to understand forecast reliability
- **Export Functionality**: Download your forecasts as CSV files
- **No Technical Knowledge Required**: Perfect for business owners who want data-driven insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 16+

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SalesForecaster
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd ReactFrontEnd
   npm install
   cd ..
   ```

### Running the Application

1. **Start both backend and frontend with one command**
   ```bash
   python app.py
   ```

2. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:5000/docs

## 🧪 Testing

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/test_preprocess.py tests/test_forecast.py

# Integration tests
pytest tests/test_integration.py

# With coverage report
pytest --cov=App --cov=FlaskBackend --cov-report=html
```

### Test Coverage
The test suite includes:
- **Unit Tests**: Individual function testing
- **Integration Tests**: Full workflow testing
- **Error Handling**: Edge cases and invalid inputs
- **Data Quality**: Validation and cleaning logic
- **Model Selection**: AI model choice logic

## 📖 How to Use

### Step 1: Upload Your Data
- Click "Upload a file" or drag and drop your CSV file
- Your CSV should have columns for dates and sales amounts
- We'll automatically detect and clean your data
- **Supported formats**: Date columns (Date, Order Date, Time), Sales columns (Sales, Revenue, Amount, Total)

### Step 2: Review Data Quality
- Check data quality insights and potential issues
- View pattern analysis (weekly trends, seasonal patterns)
- Understand how your data characteristics affect forecasting

### Step 3: Review Your Data
- Check that your data looks correct after cleaning
- Dates are formatted properly
- Sales amounts are numeric

### Step 4: Generate Forecast
- Click "Generate Forecast" to run the AI models
- Choose between automatic model selection or specify a model
- View educational insights about model selection

### Step 5: View Results
- See your sales forecast with confidence intervals
- Blue line = historical data
- Green dashed line = predicted sales
- Shaded area = confidence range
- Export results as CSV for further analysis

## 🤖 AI Models Explained

### Prophet Model
- **Best for**: Datasets with 30+ data points and seasonal patterns
- **Capabilities**: Handles trends, seasonality, and holidays automatically
- **When used**: Automatically selected for larger datasets or when weekly patterns are detected

### Linear Regression
- **Best for**: Smaller datasets (10-30 data points) without strong seasonal patterns
- **Capabilities**: Uses past 3 days to predict next 7 days
- **When used**: Automatically selected for smaller datasets without clear patterns

### Model Selection Logic
The AI automatically chooses the best model based on:
- **Data size**: More data = Prophet, Less data = Linear Regression
- **Pattern detection**: Weekly patterns trigger Prophet selection
- **Data quality**: Missing data or outliers may affect model choice

## 📊 Understanding Your Results

### Confidence Intervals
- **Narrow bands**: High confidence in predictions
- **Wide bands**: Lower confidence, consider collecting more data
- **95% confidence**: Predictions fall within this range 95% of the time

### Data Quality Insights
- **Missing values**: Rows with missing sales data are excluded
- **Outliers**: Unusually high/low values that may affect accuracy
- **Date gaps**: Missing days in your data sequence
- **Volatility**: How much your sales vary day-to-day

### Pattern Analysis
- **Weekly patterns**: Sales higher/lower on certain days of the week
- **Trends**: Overall direction of sales (increasing/decreasing)
- **Seasonality**: Repeating patterns over time

## 📁 Sample Data

Try the application with the included sample data:
- `data/preprocesstester.csv` - 45 days of realistic e-commerce data
- `data/sample_sales.csv` - 30 days of sample sales data

## 🔧 Technical Details

### Backend (Flask + Python)
- **Data Cleaning**: Automatic column detection and data normalization
- **ML Models**: 
  - Prophet (for seasonal/time-series data)
  - Linear Regression (for simpler datasets)
  - Auto-selection based on data characteristics
- **API**: RESTful endpoints with automatic documentation
- **Error Handling**: Comprehensive validation and helpful error messages

### Frontend (React + Vite)
- **Modern UI**: Built with React and Tailwind CSS
- **Interactive Charts**: Beautiful visualizations with Recharts
- **Responsive Design**: Works on desktop and mobile
- **Educational Elements**: Tooltips and explanations throughout

### Machine Learning
- **Prophet**: Facebook's time series forecasting model
- **Linear Regression**: Simple but effective for small datasets
- **Model Selection**: Automatically chooses the best model for your data
- **Confidence Assessment**: Evaluates prediction reliability

## 🚀 Deployment

### Quick Deployment
```bash
# Using Docker (recommended)
docker-compose up -d

# Manual deployment
python app.py  # Development
gunicorn FlaskBackend.run:app  # Production
```

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Docker deployment
- Cloud deployment (AWS, Heroku)
- Environment configuration
- Security considerations
- Monitoring and logging

## 🎯 Use Cases

Perfect for:
- **Small business owners**: Understand sales trends and plan inventory
- **E-commerce stores**: Predict demand and optimize marketing
- **Retail businesses**: Forecast seasonal sales patterns
- **Service providers**: Plan staffing and resources
- **Anyone wanting to predict future sales**: Data-driven decision making

## 🧪 Testing & Quality Assurance

### Test Coverage
- **Unit Tests**: 90%+ coverage of core functions
- **Integration Tests**: Full workflow testing
- **Error Handling**: Comprehensive edge case testing
- **Data Validation**: Input validation and quality checks

### Code Quality
- **Type Hints**: Full type annotation for better code quality
- **Documentation**: Comprehensive docstrings and comments
- **Error Messages**: User-friendly error messages with guidance
- **Code Style**: Consistent formatting with Black and Ruff

## 🤝 Contributing

This is a beginner-friendly project! Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Improve documentation
- Submit pull requests

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
npm install --prefix ReactFrontEnd

# Run tests
python run_tests.py

# Format code
black App/ FlaskBackend/ tests/
ruff check --fix App/ FlaskBackend/ tests/
```

## 📄 License

MIT License - feel free to use this project for your own business!

---

**Built with ❤️ for small businesses**

*Upload your CSV • Get instant forecasts • Make better decisions*

## 📞 Support

For questions or issues:
1. Check the [deployment guide](DEPLOYMENT.md)
2. Review error messages for guidance
3. Test with sample data first
4. Open an issue on GitHub