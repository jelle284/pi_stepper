import trajectory
import pigpio
import time

PUL = 26

PPR = 800
NONE = 0

def make_chunks(steps, size=1000):
    N = int(len(steps)/size) + 1
    chunks = []
    for i in range(N):
        ibegin = size*i
        iend   = min(ibegin+size, len(steps))
        if ibegin >= iend:
            break
        chunk = steps[ibegin:iend]
        chunks.append(chunk)
    return chunks

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

def move(pos, vel=5, accel=10, jerk=20):
    coeffs = trajectory.calc_coeffs(pos, jerk, accel, vel)
    steps = trajectory.step_trajectory(coeffs, PPR)
    chunks = make_chunks(steps)
    waveforms = [make_wf(chunk) for chunk in chunks]
    transmit_sync(waveforms)

def constant_vel(vel):
    pi = pigpio.pi()
    pi.set_mode(PUL, pigpio.OUTPUT)
    assert(pi.connected == 1)
    if vel > 0:
        pi.wave_clear()
        wf = []
        ts = int(1e6/(vel*PPR))
        wf.append(pigpio.pulse(1<<PUL, NONE, int(ts/2)))
        wf.append(pigpio.pulse(NONE, 1<<PUL, int(ts/2)))
        pi.wave_add_generic(wf)
        wave = pi.wave_create()
        pi.wave_send_repeat(wave)
    elif vel == 0:
        pi.wave_tx_stop()