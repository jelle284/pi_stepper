# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:05:59 2023

@author: Jelle
"""

# equation of motions
def q(a,b,c,d,t):
    return a/6 * t**3 + b/2 * t**2 + c*t + d
def qd(a,b,c,t):
    return a/2*t**2+b*t+c
def qdd(a,b,t):
    return a*t+b
def qddd(a):
    return a

# calculation of coefficients
def calc_coeffs(qf, jmax=20, amax=10, vmax=5):
    # coefficients
    t = [0]*7
    a = [0]*7
    b = [0]*7
    c = [0]*7
    d = [0]*7
    
    # given parameters
    a[0] = jmax
    a[2] = -jmax
    a[4] = -jmax
    a[6] = jmax
    
    b[1] = amax
    b[5] = -amax
    
    c[3] = vmax
    
    # calculate 1st half
    t[0] = amax/jmax
    t[1] = vmax/amax
    t[2] = t[0] + t[1]
    
    b[2] = qdd(a[1], b[1], t[1]) - qdd(a[2], 0, t[1])
    for i in range(1,3):
        c[i] = qd(a[i-1], b[i-1], c[i-1], t[i-1]) - qd(a[i], b[i], 0, t[i-1])
        d[i] = q(a[i-1], b[i-1], c[i-1], d[i-1], t[i-1]) - q(a[i], b[i], c[i], 0, t[i-1])
    
    
    # distance at beginning of constant velocity
    q2t2 = q(a[2], b[2], c[2], d[2], t[2])
    assert(qf > 2*q2t2)
    
    # calculate remaining values
    t[6] = 2*t[2] + (qf-2*q2t2)/vmax
    t[3] = t[6]-t[2]
    t[4] = t[6]-t[1]
    t[5] = t[6]-t[0]
    
    b[4] = qdd(a[3], b[3], t[3]) - qdd(a[4], 0, t[3])
    b[6] = qdd(a[5], b[5], t[5]) - qdd(a[6], 0, t[5])
    for i in range(4,7):
        c[i] = qd(a[i-1], b[i-1], c[i-1], t[i-1]) - qd(a[i], b[i], 0, t[i-1])
    for i in range(3,7):
        d[i] = q(a[i-1], b[i-1], c[i-1], d[i-1], t[i-1]) - q(a[i], b[i], c[i], 0, t[i-1])
    
    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "t": t
        }
    
# evaluate piecewise polynomial
def eval_piecewise(coeffs, t):
    if t <= 0:
        return 0, 0, 0, 0
    if t > coeffs["t"][-1]:
        a = coeffs["a"][-1]
        b = coeffs["b"][-1]
        c = coeffs["c"][-1]
        d = coeffs["d"][-1]
        tv = coeffs["t"][-1]
        return q(a,b,c,d,tv), 0, 0, 0
    for i in range(len(coeffs["t"])):
        if t <= coeffs["t"][i]:
            a = coeffs["a"][i]
            b = coeffs["b"][i]
            c = coeffs["c"][i]
            d = coeffs["d"][i]
            return q(a,b,c,d,t), qd(a,b,c,t), qdd(a,b,t), qddd(a)

# generate steps for trajectory
def step_trajectory(coeffs, step_resolution):
    steps = []
    tf = coeffs["t"][-1]
    t = 0
    x = 0
    dt = 0.005
    while t < tf:
        t += dt
        p, v, a, j = eval_piecewise(coeffs, t)
        delta = p-x
        n_steps = int(delta*step_resolution)
        x += n_steps/step_resolution
        for i in range(n_steps):
            steps.append(1e6*dt/n_steps)
    return steps
