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
    print("OK")
except ImportError:
    print("FAILED")
    print("Could not import flask, is it installed?")
    sys.exit(1)

def get_bloomberg_session(server_host = 'localhost', server_port = 8194):
    options = blpapi.SessionOptions()
    options.setServerHost(server_host)
    options.setServerPort(server_port)
    return blpapi.Session(options)

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "Hello, world."

@app.route("/session/")
def session():
    sess = get_bloomberg_session()
    sess.start()
    return "Hello, world."

def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse(sys.argv[1:])
    app.debug = args.debug
    app.run()
