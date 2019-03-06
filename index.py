import urllib

from flask import Flask, request, redirect, jsonify, send_from_directory
from twilio.twiml.messaging_response import Message, MessagingResponse
from flask_cors import CORS
from datetime import datetime
import json

from modules.Runner import runner, runner_api

app = Flask(__name__, static_folder='build/')

CORS(app);

@app.route("/", methods=["GET"])
def index():
    query = "50077"
    if request.args.get("query"):
        #cut first and last characters because 
        #GET params some how keeps quotes: '"' around its string
        query = request.args.get("query")[1:-1];
    data = runner_api(query)
    return jsonify(data)

@app.route("/api", methods=["GET"])
def api_bus():
    query = "50077"
    if request.args.get("query"):
        #cut first and last characters because 
        #GET params some how keeps quotes: '"' around its string
        query = request.args.get("query")[1:-1];
    data = runner_api(query)
    return jsonify(data)

@app.route("/sms", methods=["POST"])
def sms():
    number = request.form["From"] 
    message_body = request.form["Body"]
    
    response_data = runner(message_body)

    resp = MessagingResponse()
    resp.message(response_data);
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

@app.route("/logger", methods=["GET"])
def api_logger():
    # add 7 hours to see viet nam
    with open("ips.txt", "a") as f: 
        current = {};
        current["ip"]=request.remote_addr
        current["time"]=str(datetime.utcnow())
        current["back"]=str(request.args.get("ip"))
        current["page"]=str(request.args.get("ip1"))
        current["platform"]=str(request.args.get("platform"))
        current["agent"]=str(request.args.get("agent"))
        f.write(","+json.dumps(current));
    return jsonify({});

@app.route("/samsonhotel", methods=["GET"])
def api_samsonhotel():
    data = "";
    with open("ips.txt", "r") as f: 
        data=f.read();
    return "["+data+"]";

@app.route('/samson',methods=["GET"])
def samson():
    return send_from_directory('build/','index.html')

@app.route('/static/<path:path>',methods=["GET"])
def static_serve(path=''):
    return send_from_directory('build/static/',path)
