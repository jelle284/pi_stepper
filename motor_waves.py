import trajectory
import pigpio
import time
PUL = 23
PPR = 800
NONE = 0
MAX_MSG_LEN = 1000

def run_motor():
    coeffs = trajectory.calc_coeffs(5, 10, 5, 1)
    steps = trajectory.step_trajectory(coeffs, PPR)
    n_packets = len(steps)/MAX_MSG_LEN
    n_loops = int(n_packets) + 1
    pi = pigpio.pi()
    pi.set_mode(PUL, pigpio.OUTPUT)
    if not pi.connected:
        sys.exit(1)
    pi.wave_clear()
    wid = []
    t0 = time.time()
    for i in range(n_loops):
        ibegin = MAX_MSG_LEN*i
        iend   = min(MAX_MSG_LEN*(i+1), len(steps))
        if ibegin >= iend:
            break
        packet = steps[ibegin:iend]
        wf = []
        for step in packet:
            wf.append(pigpio.pulse(1<<PUL, NONE, int(step/2)))
            wf.append(pigpio.pulse(NONE, 1<<PUL, int(step/2)))
        pi.wave_add_generic(wf)
        traj = pi.wave_create()
        pi.wave_send_once(traj)
        while pi.wave_tx_busy(): pass
        pi.wave_delete(traj)
    elapsed = time.time() - t0
    tf = coeffs["t"][-1]
    print(f"took {elapsed} seconds, target was {tf}")
    pi.stop()

run_motor()
