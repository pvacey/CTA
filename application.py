from flask import Flask, render_template, Markup, request
import cta
application = Flask(__name__)
# application.run(debug=True)


@application.route('/')
def hello_world():
    print request.headers.get('User-Agent').lower()
    data = cta.print_next_arrivals(30116, "Blue", "Forest Park")
    return render_template('ninja.html', data=Markup(data))

@application.route('/<line>')
def get_route(line):
    return render_template('ninja.html', data="CTA %s Line\n" % line)

@application.route('/<line>/<station>')
def get_station(line, station):
    return render_template('ninja.html', data="CTA %s Line, %s station" % (line, station))
