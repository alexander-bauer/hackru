#!/usr/bin/env python2

from __future__ import print_function
import sys
import argparse
import json
import ssl
import urllib2

data = {
    "securities": ["IBM US Equity", "AAPL US Equity", "MMM US Equity"],
    "fields": ["PX_LAST", "OPEN", "EPS_ANNUALIZED"],
    "startDate": "20150416",
    "endDate": "20150418",
    "periodicitySelection": "DAILY"
}

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

def request():
    req = urllib2.Request('https://http-api.openbloomberg.com/request?ns=blp&service=refdata&type=HistoricalDataRequest')
    req.add_header('Content-Type', 'application/json')

    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_verify_locations('keys/bloomberg.crt')
    ctx.load_cert_chain('keys/client.crt', 'keys/client.key')

    try: 
        res = urllib2.urlopen(req, data=json.dumps(data), context=ctx)
        #print(res.read())
        return res
    except Exception as e:
        raise(e)

app = flask.Flask(__name__)
app.secret_key = "deadly hackathons"
login_manager = flask.ext.login.LoginManager()
login_manager.init_app(app)

@app.route('/session')
def session():

    try:
        obj = json.loads(request().read())
        return render_template("viewData.html", posts = obj)
    except Exception as e:
        print(e)
    
@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/session/")
# def session():
   
    
#     return 

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
    parser.add_argument("--remote", default='localhost')
    parser.add_argument("--remoteport", default=8194)
    parser.add_argument("--host", default='0.0.0.0')
    parser.add_argument("--port", default=80, type=int)
    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse(sys.argv[1:])
    #request()
    app.debug = args.debug
    app.run(host=args.host, port=args.port)
