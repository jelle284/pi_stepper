
import trajectory
import pigpio

PUL = (21,16,19)
PPR = 800
NONE = 0


def make_wf(steps, ax):
    wf = []
    for step in steps:
        wf.append(pigpio.pulse(1<<PUL[ax], NONE, int(step/2)))
        wf.append(pigpio.pulse(NONE, 1<<PUL[ax], int(step/2)))
    return wf

def transmit_sync(waveforms):
    pi = pigpio.pi()
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

def move(pos, vel, accel, jerk):
    pi = pigpio.pi()
    assert(pi.connected == 1)

    for pin in PUL:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.write(pin, 0)
    
    path = trajectory.SCurve(pos, jerk, accel, vel)
    move = trajectory.move(path)

    wfs = [make_wf([pw]*ns, 0) for pw, ns in move]
    transmit_sync(wfs)
    