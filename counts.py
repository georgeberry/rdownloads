from flask import Flask, redirect, render_template

import worker

import threading
import urllib2, gzip, csv, datetime, time

#flask globals

app = Flask(__name__)

a = worker.date_query(datetime.date(2014,1,1))
t1 = threading.Thread(target=a.run)
t1.start()

#flask
@app.route('/')
def draw_counts():

    try:
        with open('counts.txt', 'rb') as f:
            counts = f.read()
    except:
        counts = 0

    return "There have been {} downloads of Blaunet".format(counts)