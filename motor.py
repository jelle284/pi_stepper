
import trajectory
import pigpio
import time

PUL = (21,16,19)
PPR = 800
NONE = 0

def make_wf(chunk):
    wf = []
    for step in chunk:
        wf.append(pigpio.pulse(1<<PUL, NONE, int(step/2)))
        wf.append(pigpio.pulse(NONE, 1<<PUL, int(step/2)))
    return wf

def transmit_sync(waveforms):
    pi = pigpio.pi()
    pi.set_mode(PUL, pigpio.OUTPUT)
    assert(pi.connected == 1)
    # send first wave
    pi.wave_clear()
    pi.wave_add_generic(waveforms[0])
    w_now = pi.wave_create()
    pi.wave_send_once(w_now)
    # send consecutive waves
    for wf in waveforms[1:]:
        pi.wave_add_generic(wf)
        w_next = pi.wave_create()
        pi.wave_send_using_mode(w_next, pigpio.WAVE_MODE_ONE_SHOT_SYNC)
        while pi.wave_tx_at() == w_now:
            pass
        pi.wave_delete(w_now)
        w_now = w_next
    pi.stop()
