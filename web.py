from flask import Flask
from flask import render_template
import cta
app = Flask(__name__)

@app.route('/')
def hello_world():
    data = cta.print_next_arrivals(30116, "Blue", "Forest Park")
    return render_template('ninja.html', data=data)
