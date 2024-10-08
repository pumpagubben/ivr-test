from flask import Flask, json, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix

newCallivr = {"action": "ivr"}

callIVR_body = [1,{"dtmf":{"maxDigits":3, "terminationKey": "#"},"phrases":[{"format":"awstts","awsTTSParameters" : {"Text": "Hello again, welcome to this test. Press digits to get connected.","OutputFormat": "pcm","VoiceId": "Kendra","LanguageCode" : "en-US"}}], "hangup":False}]
callIVR_body.append({"dtmf":{"maxDigits": 3, "terminationKey": "#"}, "bargeIn": "all", "phrases": [{ "format": "file", "fileName": "test-landsa" }], "hangup": False })
callIVR_body.append({"dtmf":{"maxDigits": 5, "terminationKey": "#"}, "bargeIn": "all", "phrases": [{ "format": "file", "fileName": "landsa" }], "hangup": False })

api = Flask(__name__)

@api.route('/newCall', methods=['POST'])
def newCall_ivr():
    r = Response(response=json.dumps(newCallivr), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json;charset=utf-8"
    #print(request.json)
    print("NewCall")
    print("SessionID: " + request.json['sessionId'])
    print("CallID: " + request.json['sipCallId'])
    return r

@api.route('/callAnswered', methods=['POST'])
def callAnswered():
    print("Answered")
    return {}

@api.route('/callEvent', methods=['POST'])
def callEvent():
    print("Call Event")
    body = {}
    if request.json['event'] == "callingPartyDrop":
        body['action'] = "drop"
    print("Event: " + request.json['event'])
    if "reason" in request.json.keys():
        print("Reason: " + request.json['reason'])
    r = Response(response=json.dumps(body), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json;charset=utf-8"
    return r

@api.route('/sessionCompleted', methods=['POST'])
def sessionComplete():
    print("SessionComplete")
    print("Session duration: " + str(request.json['sessionDuration']))
    return {}

@api.route('/callNotify', methods=['POST'])
def callNotify():
    print("CallNotify")
    resp=request.json
    print(resp['sessionId'])
    print(resp['event'])
    return {}

@api.route('/getIvrCommand', methods=['POST'])
def ivrCommand():
    print("IVR-Command")
    resp=request.json
    for key in resp.keys():
        if key == "dtmfParams":
            print("DTMF Match: ")
            for key2 in resp[key].keys():
                print(key2 + ": " + resp[key][key2])
    r = Response(response=json.dumps(callIVR_body[callIVR_body[0]]), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json;charset=utf-8"
    callIVR_body[0] +=1
    if callIVR_body[0] >= len(callIVR_body):
       callIVR_body[0] = 1
    #print(request.json)
    #print(request.json['sessionId'])
    return r



if __name__ == '__main__':
    api.wsgi_app = ProxyFix(api.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    api.run(host="0.0.0.0", port=5080, debug=False)
