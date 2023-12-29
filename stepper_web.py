# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 22:08:29 2023

@author: Jelle
"""
import motor
from flask import Flask
from flask import render_template
from flask import redirect


app = Flask("Pi Stepper")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/move/<pos>")
def move(pos):
    motor.move(pos, 10, 20, 60)
    return redirect("/")