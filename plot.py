import trajectory
from matplotlib import pyplot as plt

#########################################
coef = trajectory.SCurve(20)
tfinal = coef.t[-1]

#########################################
# using polynomial evaluation
n=1000
Pp = []
Tp = []

for i in range(n):
    tp = i*tfinal/n
    pp = coef(tp)
    Tp.append(tp)
    Pp.append(pp)
    
plt.plot(Tp, Pp, label="poly")

#########################################
# using full steps list
res = 800
steps = trajectory.step_trajectory(coef, res)

Ps = []
ps = 0
Ts = []
ts = 0

for s in steps:
    ps = ps + 1 / res
    ts = ts + s * 1e-6
    Ps.append(ps)
    Ts.append(ts)

plt.plot(Ts, Ps, label="steps")
#########################################
# using chunks
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

Pc = []
pc = 0
Tc = []
tc = 0
chunks = make_chunks(steps)
for c in chunks:
    for s in c:
        pc = pc + 1 / res
        tc = tc + s * 1e-6
        Pc.append(pc)
        Tc.append(tc)

plt.plot(Tc, Pc, "r--", label="chunks")

#########################################
# using partial time stepping
Pt = []
pt = 0
Tt = []
tt = 0

moves = trajectory.move(coef, 20)

for m in moves:
    ns, pw = m
    for s in range(ns):
        pt = pt + 1 / res
        tt = tt + pw
        Pt.append(pt)
        Tt.append(tt)
        
plt.plot(Tt, Pt, "k--", label="partial")

##########################################
# show figure
plt.grid()
plt.legend()
plt.show()