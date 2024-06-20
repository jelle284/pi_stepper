import pigpio
import time


moves = ((1<<21, 200, 600),
        (1<<16, 80, 1000),
        (1<<19, 120, 800))

pi = pigpio.pi()
assert(pi.connected == 1)
pi.wave_clear()

for pin, nsteps, delayus in moves:
    wf = []
    for n in range(nsteps):
        wf.append(pigpio.pulse(pin, 0, int(delayus/2)))
        wf.append(pigpio.pulse(0, pin, int(delayus/2)))
    pi.wave_add_generic(wf)
    
wid = pi.wave_create()
pi.wave_send_once(wid)

while pi.wave_tx_busy():
    time.sleep(0.1)
    
pi.stop()