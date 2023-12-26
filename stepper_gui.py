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
import motor_wavesync as motor
    
class Gui:
    def __init__(self, window):
        self.btn = tk.Button(text="Run motor", command=self.cb_run_motor)
        self.btn.pack()
        self.ent = tk.Entry(width=20)
        self.ent.pack()
        
    def cb_run_motor(self):
        distance = int(self.ent.get())
        motor.move(distance)

def main(args):
    window = tk.Tk()
    gui = Gui(window)
    window.mainloop()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
