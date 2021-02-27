from flask import Flask, current_app, request
from pump import *

app = Flask(__name__)

@app.route('/')
def index():
    return current_app.send_static_file('./index.html')

@app.route('/visualize', methods = ['POST'])
def visualize():
    return main_pump(request.json)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

