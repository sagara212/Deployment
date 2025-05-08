from flask import Flask, render_template, request
import requests
import os 
os.environ['NO_PROXY'] = '127.0.0.1, localhost'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sepal_length = request.form['sepal_length']
        sepal_width = request.form['sepal_width']
        petal_length = request.form['petal_length']
        petal_width = request.form['petal_width']

        payload = {
            'sepal_length': sepal_length,
            'sepal_width': sepal_width,
            'petal_length': petal_length,
            'petal_width': petal_width
        }
        
        # Kirim ke FastAPI
        response = requests.post('http://127.0.0.1:8000/predict', json=payload)
        result = response.json()

        return render_template('result.html', prediction=result['prediction'], confidence=result['confidence'])
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
