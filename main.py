#!/usr/bin/env python2

from __future__ import print_function
import sys
import argparse

print("Importing blpapi... ", end="")
try:
    import blpapi
    print("OK")
except ImportError:
    print("FAILED")
    print("Could not import blpapi, is it installed?")
    sys.exit(1)

print("Importing flask... ", end="")
try:
    import flask
    from flask import render_template, g, request, redirect
    print("OK")
except ImportError:
    print("FAILED")
    print("Could not import flask, is it installed?")
    sys.exit(1)

print("Importing flask-login... ", end="")
try:
    import flask.ext.login
    print("OK")
except ImportError:
    print("FAILED")
    print("Could not import flask-login, is it installed?")
    sys.exit(1)

def get_bloomberg_session(server_host = 'localhost', server_port = 8194):
    options = blpapi.SessionOptions()
    options.setServerHost(server_host)
    options.setServerPort(server_port)
    return blpapi.Session(options)

def start_request_service(session):
    requestID = CorrelationID(1)
    refDataSvc = session.getService("//blp/refdata")
    request = refDataSvc.createRequest("RefrenceDataRequest")
    request.append("securities","IMB US Equity")
    request.append("fields","PX_LAST")
    session.sendRequest(request,requestID)
    flag = True
    while (flag):
        event = session.nextEvent()
        if (event.eventType().intValue()==Event.EventType.Constants.RESPONSE):
            flag = False
        elif(event.eventType().intValue()== Event.EventType.Constants.PARTIAL_RESPONSE):
            handleResponseEvent(event)
        else:
            handleOtherEvent(event)

def handleResponseEvent(event):
    print("EventType=" + event.eventType())
    iterate = event.messageIterator()
    while(iterate.hasNext()):
        message = iterate.next()
        print("correlationID = " + message.correlationID())
        print("messageType = " + message.messageType())
        print(str(message))


app = flask.Flask(__name__)
app.secret_key = "deadly hackathons"
login_manager = flask.ext.login.LoginManager()
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/session/")
def session():
    sess = get_bloomberg_session()
    sess.start()
    start_request_service(sess)
    return "Hello, world."

@app.route('/register', methods = ['POST'])
def register():
    form = flask.LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)

@app.route('/login', methods = ['POST'])
def login():
    form = flask.LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action='store_true')
    parser.add_argument("--host", default='0.0.0.0')
    parser.add_argument("--port", default=80, type=int)
    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse(sys.argv[1:])
    app.debug = args.debug
    app.run(host=args.host, port=args.port)
