# Django Stock Prediction and Reporting System

This project is a Django-based system that allows users to generate stock price predictions using a pre-trained machine learning model. It also generates reports (in both JSON and PDF formats) that compare predicted stock prices with actual data and include key financial metrics.

## Features
- Fetch historical stock data from the database
- Predict future stock prices using a pre-trained machine learning model
- Generate stock performance reports with key metrics and visualizations
- Downloadable reports in PDF format
- JSON API responses for programmatic consumption

## Setup and Installation

### Prerequisites

- Python 3.12+
- PostgreSQL database (or any other Django-supported database)
- Required Python packages:
  - Django
  - Pandas
  - ReportLab
  - Pillow (PIL)
  - Matplotlib

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/GlennWilliam/django_backend.git
   cd django_backend
   
2. **Create virtual env**

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows, use myenv\Scripts\activate

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt


4. **Set up database**

     DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'your_db_name',
          'USER': 'your_db_user',
          'PASSWORD': 'your_db_password',
          'HOST': 'localhost',
          'PORT': '5432',
      }

5. **Run migrations**

   ```bash
   python manage.py migrate

6. **Run the development server**

   ```bash
   python manage.py runserver

API Endpoints

1. Predict Stock Prices

	•	URL: /predict/<stock_symbol>/
	•	Method: GET
	•	Description: Fetches historical stock prices and predicts the next 30 days’ prices.
	•	Response: JSON with predicted stock prices and dates.

2. Generate Stock Report

	•	URL: /report/<stock_symbol>/?format=pdf
	•	Method: GET
	•	Description: Generates a performance report with financial metrics and actual vs predicted stock prices.
	•	Response: PDF download if format=pdf, or JSON if format is not specified.

Code Structure

	•	stocks/: Contains the core logic for stock prediction and reporting.
	•	models.py: Defines the StockData model for storing stock prices.
	•	views.py: Defines views for predicting stock prices and generating reports.
	•	utils.py: Contains utility functions for generating plots and reports.
	•	ml_model.py: Contains the machine learning logic for predicting stock prices.
	•	templates/: Contains HTML templates (if any) for rendering views.
	•	static/: Stores static files like CSS and JavaScript (if any).

  

