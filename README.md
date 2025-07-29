# 📊 Sales Forecaster

A beginner-friendly web application that helps small businesses forecast their sales using AI. Simply upload your sales data and get instant predictions!

## ✨ Features

- **Smart Data Cleaning**: Automatically detects and cleans date and sales columns from your CSV files
- **AI-Powered Forecasting**: Uses advanced machine learning models (Prophet and Linear Regression) to predict future sales
- **Beautiful UI**: Modern, intuitive interface that guides you through each step
- **Confidence Intervals**: See prediction ranges to understand forecast reliability
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

## 📖 How to Use

### Step 1: Upload Your Data
- Click "Upload a file" or drag and drop your CSV file
- Your CSV should have columns for dates and sales amounts
- We'll automatically detect and clean your data

### Step 2: Review Your Data
- Check that your data looks correct after cleaning
- Dates are formatted properly
- Sales amounts are numeric

### Step 3: Generate Forecast
- Click "Generate Forecast" to run the AI models
- Choose between automatic model selection or specify a model

### Step 4: View Results
- See your sales forecast with confidence intervals
- Blue line = historical data
- Green dashed line = predicted sales
- Shaded area = confidence range

## 📁 Sample Data

Try the application with the included sample data:
- `data/sample_sales.csv` - 30 days of sample sales data

## 🔧 Technical Details

### Backend (Flask + Python)
- **Data Cleaning**: Automatic column detection and data normalization
- **ML Models**: 
  - Prophet (for seasonal/time-series data)
  - Linear Regression (for simpler datasets)
  - Auto-selection based on data characteristics
- **API**: RESTful endpoints with automatic documentation

### Frontend (React + Vite)
- **Modern UI**: Built with React and Tailwind CSS
- **Interactive Charts**: Beautiful visualizations with Recharts
- **Responsive Design**: Works on desktop and mobile

### Machine Learning
- **Prophet**: Facebook's time series forecasting model
- **Linear Regression**: Simple but effective for small datasets
- **Model Selection**: Automatically chooses the best model for your data

## 🧪 Testing

Run the test suite to verify everything works:
```bash
python test_app.py
```

## 📊 Supported Data Formats

Your CSV file should contain:
- **Date column**: Any column with dates (e.g., "Date", "Order Date", "Time")
- **Sales column**: Any column with numeric sales data (e.g., "Sales", "Revenue", "Amount")

We automatically detect and clean:
- Various date formats
- Currency symbols and formatting
- Missing or invalid data

## 🎯 Use Cases

Perfect for:
- Small business owners
- E-commerce stores
- Retail businesses
- Service providers
- Anyone wanting to predict future sales

## 🤝 Contributing

This is a beginner-friendly project! Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Improve documentation

## 📄 License

MIT License - feel free to use this project for your own business!

---

**Built with ❤️ for small businesses**

*Upload your CSV • Get instant forecasts • Make better decisions*