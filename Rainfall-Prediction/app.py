import bz2
import pickle
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sklearn.preprocessing import LabelEncoder
import pandas as pd


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    #db.drop_all()  # Drop existing tables (if any)
    db.create_all()


@app.route('/')
def newhome():
    return render_template('newhome.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        new_user = User(email = email, password = password)
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already registered')
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html') 

@app.route('/login', methods = ['GET', 'POST'])    
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/home')    
        else:
            return render_template('login.html', error = 'Invalid User')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

@app.route('/rain_home')
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
    model_path = "Rainfall-Prediction\models\model1.pbz2"
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
    model_path = "Rainfall-Prediction\models\model4.pbz2"
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
    model_path = "Rainfall-Prediction\models\model3.pbz2"
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
    model_path = "Rainfall-Prediction\models\model2.pbz2"
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


# Load the model
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

model = decompress_pickle('Rainfall-Prediction\models\XB.pbz2')

# Load the label encoder
label_encoder = LabelEncoder()

# Load the original dataset
df = pd.read_csv("Rainfall-Prediction\Dataset\Crop_recommendation.csv")  # Update the file path accordingly

# Fit label encoder
label_encoder.fit(df['label'])

@app.route('/crop_home')
def crop_home():
    return render_template('crop_home.html')

@app.route('/crop_index')
def crop_index():
    return render_template('crop_index.html')

@app.route('/process_parameters', methods=['POST'])
def process_parameters():
    if request.method == 'POST':
        # Retrieve the form data
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # Perform prediction using the model
        predicted_crop = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

        # Convert the predicted label to human-readable format
        decoded_labels = label_encoder.inverse_transform(predicted_crop)

        # Render the result template with the predicted crop
        return render_template('crop_result.html', N=N, P=P, K=K, temperature=temperature, humidity=humidity, ph=ph, rainfall=rainfall, crop=decoded_labels[0])
    else:
        return 'Method not allowed'

if __name__ == '__main__':
    app.run(debug=True)
