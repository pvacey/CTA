from flask import Flask, render_template, Markup, request
import cta
application = Flask(__name__)

@application.route('/')
def hello_world():
    return output(request, cta.get_term_lines())

@application.route('/<line>')
def get_line(line):
    return output(request, cta.get_term_line_stations(line))

@application.route('/<line>/<station>')
def get_times(line, station):
    return output(request, cta.get_term_arrivals(line_name=line,
                                                 station_name=station))

def output(requests, data):
    """Decide how to present the data to the user based on user agent"""
    user_agent = request.headers.get('User-Agent').lower()
    if user_agent.startswith('curl'):
        return data
    else:
        return '<pre> {} </pre>'.format(data)

if __name__ == '__main__':
    application.run(debug=True)
