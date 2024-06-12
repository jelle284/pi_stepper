import trajectory
from matplotlib import legend, pyplot as plt

#########################################
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


res = 800

coef = trajectory.calc_coeffs(20)

steps = trajectory.step_trajectory(coef, res)
#########################################
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
n=1000
Pp = []
Tp = []
tf = coef["t"][-1]
for i in range(n):
    tp = i*tf/n
    pp = trajectory.eval_piecewise(coef, tp)
    Tp.append(tp)
    Pp.append(pp[0])
    
plt.plot(Tp, Pp, label="poly")

#########################################
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

plt.grid()
plt.legend()
plt.show()