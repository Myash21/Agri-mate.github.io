import bz2
import pickle
from flask import Flask, render_template, request


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
app = Flask(__name__)
 

@app.route('/')
def ground0():
    return render_template('ground0.html')


# Render the home page
@app.route('/home')
def home():
    return render_template('home.html')

# Render the Konkan region page
@app.route('/konkan')
def konkan():
    return render_template('konkan.html')

# Handle the form submission for Konkan region prediction
@app.route('/konkan_prediction', methods=['POST'])
def konkan_prediction():
    model_path = "models/model1.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months']) 
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)  # Corrected: 'konkan_result.html' instead of 'result.html'
    else:
        return 'Invalid request'




@app.route('/vidarbha')
def vidarbha():
    return render_template('vidarbha.html')

@app.route('/vidarbha_prediction', methods=['POST'])
def vidarbha_prediction():
    model_path = "models/model4.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months']) 
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)   
    else:
        return 'Invalid request'
    

@app.route('/marathwada')
def marathwada():
    return render_template('marathwada.html')

@app.route('/marathwada_prediction', methods=['POST'])
def marathwada_prediction():
    model_path = "models/model3.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months']) 
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)  
    else:
        return 'Invalid request'


@app.route('/madhya_maharashtra')
def madhya_maharashtra():
    return render_template('madhya_maharashtra.html')

@app.route('/madhya_maharashtra_prediction', methods=['POST'])
def madhya_maharashtra_prediction():
    model_path = "models/model2.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months']) 
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results) 
    else:
        return 'Invalid request'



if __name__ == '__main__':
    app.run(debug=True)
