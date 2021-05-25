"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request, jsonify
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import os
#import docker
import json
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb


#### install docker

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.route("/submit", methods=["POST"])
def submit():
    #filled = []
    data = json.loads(request.form.get('submit_data'))
    app.logger.debug("GOT GOT POST POST")

   
    #for row in data:
    #    #print(row)
    #    if row !={'date': '2021-01-01T00:00', 'dist': '200', 'miles': '', 'km': '', 'open': '', 'close': '', 'location': ''}:
    #        print("valid rows: ",row)
    #        if row not in filled:
    #            filled.append(row)
    #print("new list: ", filled)
    #print(len(filled))
    #newdict = {}
    db.tododb.drop()
    for i in data:
        db.tododb.insert_one(i)
    #for i in range(len(filled)):
    #    newdict[i] = filled[i]
    #print("newdict: ", newdict)
    #db.tododb.insert_one(newdict)
    #render_template('calc.html', vals=list(db.tododb.find()))
    message = "HEEEEEYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

        #go through, insert valid rows in db
        #use drop/remove
    
    print("DATA DATA DATA: ",data)
    ## DATA IS A LIST

    ###return some string show that submit worked
    return flask.jsonify(message)


@app.route("/display")
def display():
    print("WHAT IS BEING SENT TO DISPLAY: ",list(db.tododb.find()) )
    return flask.render_template("display.html", info=list(db.tododb.find()))

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', type=float)
    distance = request.args.get('distance', type=float )
    begin_date = request.args.get('begin_date', type=str)
    print(begin_date)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!

    date = arrow.get(begin_date, 'YYYY-MM-DDTHH:mm')

    ##

    open_time = acp_times.open_time(km, distance, date).format('YYYY-MM-DDTHH:mm')

    close_time = acp_times.close_time(km, distance, date).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
