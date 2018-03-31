import urllib

from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import Message, MessagingResponse

from modules.Runner import runner

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    query = "50077"
    if request.args.get("query"):

        #cut first and last characters because 
        #GET params some how keeps quotes: '"' around its string
        query = request.args.get("query")[1:-1];
    data = runner(query)
    return data


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

