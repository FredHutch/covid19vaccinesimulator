# fix windows registry stuff
import mimetypes
mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from datetime import datetime


# version 1
# from flask import Flask, jsonify, request

# version 2
import time
from flask import Flask, request, jsonify, current_app, g as app_context

# from python_script import example 
from python_script import example_finalModel as example
import json
from datetime import datetime

# app = Flask(__name__, static_folder='app', static_url_path="/")

# integrated with front
app = Flask(__name__, static_folder='dist', static_url_path="/")

print(mimetypes.knownfiles)
print(mimetypes.types_map['.js'])
print(mimetypes.types_map['.css'])

log_file_name = "{}.txt".format(datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))

def writeLog(msg):
    f = open("./log/" + log_file_name, "a")
    now = datetime.now() # current date and time
    # '2011-11-04T00:05:23'
    time_string = now.strftime("%m-%d-%YT%H:%M:%S")
    f.write(f"[{time_string}] {msg}\n")
    f.close()

@app.before_request
def logging_before():
    # Store the start time for the request
    app_context.start_time = time.perf_counter()
    print("start_time: {}".format(app_context.start_time))


@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_context.start_time
    print("total_time: {}".format(total_time))
    writeLog("[total_time] {}".format(total_time))
    time_in_ms = int(total_time * 1000)
    print("time_in_ms: {}".format(time_in_ms))
    # Log the time taken for the endpoint 
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response

@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})


def is_valid_input(input):
    result = True

    input_json = input # json.loads(input)

    input_keys = input_json.keys()

    print(input_keys)

    if( "simulationInterval" not in input_keys):
        print("simulationInterval" + "not in input_keys")
        result = False
    elif( "regionParameters" not in input_keys):
        result = False
    elif( "vaccineParameters" not in input_keys):
        result = False
    elif( "fixedParameters" not in input_keys):
        result = False

    print("is_input_valid: " + str(result))
    return result

# @app.route('/simulation', methods=['GET', 'POST'])
@app.route('/simulation', methods=['POST'])
# @app.route('/simulation')
def simulation():
    print("/simulation starts")
    result = {}

    for key,value in request.headers.items():
        msg = f"[headers]: {key} - {value}"
        print(msg)
    # writeLog(msg)
    

    data = request.json
    msg = f"[input]: {json.dumps(data)}"
    #print(msg)
    writeLog(msg)
    strategyIndex = data["index"]
    #print(f"data.keys: {data.keys()}")

    if( is_valid_input(data)):
        result = example.main(data)

    writeLog(f"[result]: {result}")
    result["index"] = strategyIndex

    #print(f"response: {json.dumps(result)}")
    print("/simulation ends")
    return jsonify(result)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print("index.html")
    return app.send_static_file("index.html")