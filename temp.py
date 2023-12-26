#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  temp.py
#  
#  Copyright 2023  <raspberry@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import tkinter as tk
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
    
def main(args):
    window = tk.Tk()
    btn = tk.Button(text="Run motor", command=run_motor)
    btn.pack()
    ent = tk.Entry(width=20)
    window.mainloop()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
