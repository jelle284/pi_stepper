import pigpio
import time


moves = ((1<<21, 200, 600),
        (1<<16, 80, 1000),
        (1<<19, 120, 800))

pi = pigpio.pi()
assert(pi.connected == 1)
pi.wave_clear()
first = True
wold = -1
for i in range(56):
    for pin, nsteps, delayus in moves:
        wf = [pigpio.pulse(pin, 0, int(delayus/2)), pigpio.pulse(0, pin, int(delayus/2))]*nsteps
        pi.wave_add_generic(wf)
    wid = pi.wave_create_and_pad(25)
    if first:
        pi.wave_send_once(wid)
        wold = wid
        first = False
        continue
    pi.wave_send_using_mode(pigpio.WAVE_MODE_ONE_SHOT_SYNC)
    while pi.wave_tx_at == wold:
        time.sleep(0.01)
    pi.wave_delete(wold)
    wold=wid
    
pi.stop()