import motor

def main(args):
    print(args)
    if len(args) > 1:
        pos = float(args[1])
    else:
        pos = 33
    if len(args) > 2:
        vel = float(args[2])
    else:
        vel = 10
    if len(args) > 3:
        accel = float(args[3])
    else:
        accel = 20
    if len(args) > 4:
        jerk = float(args[4])
    else:
        jerk = 60
    motor.move(pos, vel, accel, jerk)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
