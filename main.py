import urllib.request, urllib.error, urllib.parse, json
from flask import Flask, render_template, request
from datetime import date
import datetime
import random

app = Flask(__name__)
start_date = datetime.datetime.strptime('1995-6-16', "%Y-%m-%d")
today = datetime.datetime.today()
# safe_get from s10
def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print(url)
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print(url)
        print("Reason: ", e.reason)
    return None

# to make more readable output of nested data structures
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('AOD.html',page_title="APOD")

def get_date_picture(date = None):
    params = {'api_key': '3LLfiNRWkl0cGAx9b3obDBRovTvmDWwJjpC3g9yU'}
    if date is not None:
        params['date'] = date
    # if date is None:
    #     params['date'] = today
    paramstr = urllib.parse.urlencode(params)
    baseurl = 'https://api.nasa.gov/planetary/apod'
    apodquest = baseurl + "?" + paramstr
    apodqueststr = urllib.request.urlopen(apodquest).read()
    apodqueststr = json.loads(apodqueststr)
    day = apodqueststr
    return day

def get_random_picture():
    params = {'api_key': '3LLfiNRWkl0cGAx9b3obDBRovTvmDWwJjpC3g9yU'}
    start_date = datetime.date(1995, 6, 16)
    end_date = date.today()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    if random_date:
        params['date'] = random_date
    paramstr = urllib.parse.urlencode(params)
    baseurl = 'https://api.nasa.gov/planetary/apod'
    apodquest = baseurl + "?" + paramstr
    apodqueststr = urllib.request.urlopen(apodquest).read()
    apodqueststr = json.loads(apodqueststr)
    day = apodqueststr
    return day

@app.route("/dateresponse")
def date_response_handler():
    app.logger.info(request.args.get('date'))
    input_date = request.args.get('date')
    # dict = {}
    if input_date == '':
        dict = get_date_picture()
    else:
        current_date = datetime.datetime.strptime(input_date, "%Y-%m-%d")
        if current_date > today or current_date < start_date:
            return render_template('dateresponse.html', invalid = True)
        dict = get_date_picture(input_date)
    return render_template('dateresponse.html', dict=dict)


@app.route("/randomresponse")
def random_response_handler():
    dict = get_random_picture()
    return render_template('randomresponse.html', dict=dict)

def get_date_picture_safe(date = None):
    try:
        return get_date_picture(date)
    except urllib.error.HTTPError as e:
        print("Error trying to retrieve data: HTTP Error " + str(e.code) + ": Bad Request")
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

if __name__ == "__main__":
    # Used when running locally only. 
	# When deploying to Google AppEngine, a webserver process
	# will serve your app. 
    app.run(host="localhost", port=4000, debug=True)