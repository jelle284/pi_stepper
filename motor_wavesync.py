import trajectory
import pigpio
import time
PUL = 23
PPR = 3200
NONE = 0
MAX_MSG_LEN = 2000

def make_chunks(steps):
	N = int(len(steps)/MAX_MSG_LEN) + 1
	chunks = []
	for i in range(N):
		ibegin = MAX_MSG_LEN*i
		iend   = min(MAX_MSG_LEN*(i+1), len(steps))
		if ibegin >= iend:
			break
		packet = steps[ibegin:iend]
		wf = []
		for step in packet:
			wf.append(pigpio.pulse(1<<PUL, NONE, int(step/2)))
			wf.append(pigpio.pulse(NONE, 1<<PUL, int(step/2)))
		chunks.append(wf)
	return chunks
	
def run_motor():
	coeffs = trajectory.calc_coeffs(20, 10, 5, 6)
	steps = trajectory.step_trajectory(coeffs, PPR)

	pi = pigpio.pi()
	pi.set_mode(PUL, pigpio.OUTPUT)
	if not pi.connected:
		sys.exit(1)
	pi.wave_clear()
	chunks = make_chunks(steps)
	t0 = time.time()
	# timed
	pi.wave_add_generic(chunks[0])
	w_now = pi.wave_create()
	pi.wave_send_once(w_now)
	for c in chunks[1:]:
		pi.wave_add_generic(c)
		w_next = pi.wave_create()
		pi.wave_send_using_mode(w_next, pigpio.WAVE_MODE_ONE_SHOT_SYNC)
		while pi.wave_tx_at() == w_now:
			time.sleep(0.1)
		pi.wave_delete(w_now)
		w_now = w_next
	# /timed
	elapsed = time.time() - t0
	tf = coeffs["t"][-1]
	print(f"took {elapsed} seconds, target was {tf}")
	pi.stop()

run_motor()

