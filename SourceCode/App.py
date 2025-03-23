from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load the machine learning model
model = pickle.load(open('C:\project AB6\Source Code\Kidney.pkl', 'rb'))

# Home Route
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# About Section
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# Predictions Section
@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    if request.method == 'POST':
        try:
            # Extract input values from the form
            int_features = [float(x) for x in request.form.values()]
            final = [np.array(int_features)]
            prediction = model.predict_proba(final)
            output = '{0:.{1}f}'.format(prediction[0][1], 2)

            # Render result based on model output
            if float(output) >= 0.5:  # Adjust threshold for CKD if needed
                return render_template('result.html', prediction="CKD Detected")
            else:
                return render_template('result2.html', prediction="No CKD Detected")
        except Exception as e:
            return render_template('error.html', error=str(e))

    # Render input form on GET request
    return render_template('image.html')

# Metrics Section
@app.route('/metrics', methods=['GET'])
def metrics():
    return render_template('metrics.html')

# Flowchart Section
@app.route('/flowchart', methods=['GET'])
def flowchart():
    return render_template('flowchart.html')

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found!"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1000, debug=True)
