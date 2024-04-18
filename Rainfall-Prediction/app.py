from flask import Flask, render_template, request
import joblib
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

# Load the ARIMA model
MODEL_PATH = "Rainfall-Prediction\\models\\model2.joblib"
model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        num_periods = int(request.form['num_periods'])
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)

if __name__ == '__main__':
    app.run(debug=True)