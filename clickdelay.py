#!/usr/bin/env python

from flask import Flask
from threading import Timer
from urllib.request import urlopen
from datetime import datetime

import configparser
config = configparser.ConfigParser()
config.read('clickdelay.ini')

app = Flask(__name__)

@app.route('/')
def index():
    f = open("html/index.html", "r")
    return f.read()

@app.route('/zirkulation')
def zirkulation():
    f = open("html/zirkulation.html", "r")
    return f.read()

@app.route('/health')
def health():
    return 'up'

@app.route('/status/<tasmota>')
def status(tasmota):
    propkey = 'tasmota.' + tasmota + '.status'
    statuslink = urlopen(config['TasmotaSection'][propkey])
    return statuslink.read().decode('utf-8')

def internalswitch(tasmota, offonly):
    if 'ON' in status(tasmota) or offonly == 0:
        propkey = 'tasmota.' + tasmota + '.switch'
        switchlink = urlopen(config['TasmotaSection'][propkey])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmota + ': ' + retval)
    else:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmota + ': already off')

@app.route('/switch/<tasmota>/<waittime>')
def switch(tasmota, waittime):
    internalswitch(tasmota, 0)
    t = Timer(float(waittime), internalswitch, [tasmota, 1])
    t.start() 
    return status(tasmota)

@app.route('/color/<tasmota>')
def color(tasmota):
    if 'ON' in status(tasmota):
        return '#DAF7A6'
    else:
        return '#FF5733'

app.run(host='0.0.0.0', port=50000)