from flask import Flask, render_template, Markup, request
import cta
app = Flask(__name__)
app.run(debug=True)


@app.route('/')
def hello_world():
    print request.headers.get('User-Agent').lower()
    data = cta.print_next_arrivals(30116, "Blue", "Forest Park")
    return render_template('ninja.html', data=Markup(data))
