###################################################################
import pigpio

PUL = (21,16,19)
DIR = (20,12,26)
NONE = 0
PPR = 800
CONST_VEL = 2

pi = pigpio.pi()

for pin in PUL+DIR:
    pi.set_mode(pin, pigpio.OUTPUT)

def constant_vel(axis, direction=0):
    if axis < 0 or axis >= len(PUL): return
    pi.write(DIR[axis], direction)
    pi.wave_clear()
    wf = []
    ts = int(1e6/(CONST_VEL*PPR))
    wf.append(pigpio.pulse(1<<PUL[axis], NONE, int(ts/2)))
    wf.append(pigpio.pulse(NONE, 1<<PUL[axis], int(ts/2)))
    pi.wave_add_generic(wf)
    wave = pi.wave_create()
    pi.wave_send_repeat(wave)
    
#########################################################################
from flask import Flask
from flask import render_template
from flask import redirect

app = Flask("Pi Stepper")

state=0

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fwd/<int:axis>")
def fwd(axis=0):
    constant_vel(axis)
    return ""

@app.route("/rev/<int:axis>")
def rev(axis=0):
    global state
    if state == 0:
        state = 1
        constant_vel(axis, direction=1)
    return ""

@app.route("/stop")
def stop():
    pi.wave_tx_stop()
    global state
    state=0
    return ""

app.run("0.0.0.0", 5000)