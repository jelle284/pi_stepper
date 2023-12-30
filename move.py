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

import motor

def main(args):
    print(args)
    if len(args) > 0:
        pos = float(args[1])
    else:
        pos = 33
    if len(args) > 1:
        vel = float(args[2])
    else:
        vel = 10
    if len(args) > 2:
        accel = float(args[3])
    else:
        accel = 20
    if len(args) > 3:
        jerk = float(args[4])
    else:
        jerk = 60
    motor.move(pos, vel, accel, jerk)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
