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
import motor
    
class Gui:
    def __init__(self, window):
        self.btn = tk.Button(text="Run motor", command=self.cb_run_motor)
        self.btn.pack()
        self.ent_pos = tk.Entry(width=20)
        self.ent_pos.insert(tk.END, "16")
        self.ent_pos.pack()
        self.ent_vel = tk.Entry(width=20)
        self.ent_vel.insert(tk.END, "10")
        self.ent_vel.pack()
        self.ent_accel = tk.Entry(width=20)
        self.ent_accel.insert(tk.END, "20")
        self.ent_accel.pack()
        self.ent_jerk = tk.Entry(width=20)
        self.ent_jerk.insert(tk.END, "60")
        self.ent_jerk.pack()
        
    def cb_run_motor(self):
        pos = float(self.ent_pos.get())
        vel = float(self.ent_vel.get())
        accel = float(self.ent_accel.get())
        jerk = float(self.ent_jerk.get())
        motor.move(pos, vel, accel, jerk)

def main(args):
    window = tk.Tk()
    gui = Gui(window)
    window.mainloop()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
