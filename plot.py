import trajectory
from matplotlib import pyplot as plt

#########################################
scurve = trajectory.SCurve(20)

#########################################
# using polynomial evaluation
n=1000
Pp = []
Tp = []

for i in range(n):
    tp = i*scurve.duration/n
    pp = scurve(tp)
    Tp.append(tp)
    Pp.append(pp)
    
plt.plot(Tp, Pp, label="poly")

#########################################
# using partial time stepping
Pt = []
pt = 0
Tt = []
tt = 0

for nsteps, pulsewidth in trajectory.move(scurve):
    for s in range(nsteps):
        pt = pt + 1 / 800
        tt = tt + pulsewidth
        Pt.append(pt)
        Tt.append(tt)
        
plt.plot(Tt, Pt, "k--", label="partial")

##########################################
# show figure
plt.grid()
plt.legend()
plt.show()