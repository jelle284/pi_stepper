import trajectory
import pigpio
import time
PUL = 23
PPR = 800

def run_motor():
	coeffs = trajectory.calc_coeffs(5, 10, 5, 1)
	steps = trajectory.step_trajectory(coeffs, PPR)
	pi = pigpio.pi()
	pi.set_mode(PUL, pigpio.OUTPUT)
	if not pi.connected:
		sys.exit(1)
	# timed motor control
	t0 = time.time()
	for step in steps:
		pi.write(PUL, 1)
		time.sleep(1e-6*step/2)
		pi.write(PUL, 0)
		time.sleep(1e-6*step/2)
	# end
	elapsed = time.time() - t0
	tf = coeffs["t"][-1]
	print(f"took {elapsed} seconds, target was {tf}")
	pi.stop()

run_motor()
