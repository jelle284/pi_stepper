###################################################################
import pigpio

PUL = (21,16,19)
DIR = (20,12,26)
NONE = 0
PPR = 800
CONST_VEL = 2

def constant_vel(axis, direction=0):
    if axis < 0 or axis >= len(PUL): return
    pi = pigpio.pi()
    pi.set_mode(PUL[axis], pigpio.OUTPUT)
    pi.set_mode(DIR[axis], pigpio.OUTPUT)
    pi.write(DIR[axis], direction)
    assert(pi.connected == 1)
    pi.wave_clear()
    wf = []
    ts = int(1e6/(CONST_VEL*PPR))
    wf.append(pigpio.pulse(1<<PUL[axis], NONE, int(ts/2)))
    wf.append(pigpio.pulse(NONE, 1<<PUL[axis], int(ts/2)))
    pi.wave_add_generic(wf)
    wave = pi.wave_create()
    pi.wave_send_repeat(wave)

def stop_all():
    pi = pigpio.pi()
    assert(pi.connected == 1)
    pi.wave_tx_stop()
    
#########################################################################
from flask import Flask
from flask import render_template
from flask import redirect

app = Flask("Pi Stepper")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fwd/<axis>")
def fwd(axis=0):
    constant_vel(axis)
    return ""

@app.route("/rev/<axis>")
def rev(axis=0):
    constant_vel(axis, direction=1)
    return ""

@app.route("/stop")
def stop():
    stop_all()
    return ""

app.run("0.0.0.0", 5000)