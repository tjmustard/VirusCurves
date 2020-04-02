__author__ = 'mustard'

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import locale
locale.setlocale(locale.LC_ALL, '')

def f(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x - d))) + b

#Days since first reported case:
x_orig = [0, 3, 4, 5, 9, 10, 11, 12, 15, 30, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
#Confirmed cases of COVID19
y_orig = [1, 2, 3, 5, 6, 7, 8, 11, 12, 14, 15, 15, 19, 24, 42, 57, 85, 111, 175, 252, 353, 497, 645, 936, 1205, 1598, 2163, 2825, 3497, 4372, 5656, 8074, 12018, 17438, 23710, 32341, 42751, 52690, 64916, 81966, 101012, 121105, 140223, 160686, 186082, 212814]

x = x_orig.copy()
y = y_orig.copy()

#Growth Phase 1
#It is known that 2019-nCov has an incubation period of ~5-14 days
#So actions today will not change the growth rate for ~5-14 days
phase1 = 10 #4 days since statewide shutdowns <---- EDIT THIS NUMBER
#Currect Growth rate is 30% or an increase of 1.3x perday
phase1_gr = 1.15 #<------ EDIT THIS NUMBER 
for i in range(1, phase1):
    x.append(x[-1] + 1)
    y.append(y[-1] * phase1_gr)

#Once precations are in place to change the spread of the virus (social distancing)
#The growth rate starts to slow down as people no longer interact and those
#who have had the virus get better and no longer infect new people
phase2 = 20 #<---- EDIT THIS NUMBER
phase2_gr = 1.1 #<---- EDIT THIS NUMBER
for i in range(1, phase2):
    x.append(x[-1] + 1)
    y.append(y[-1] * phase2_gr)

#Fit logistic curve to the known and projected data
(a_, b_, c_, d_), _ = opt.curve_fit(f, x, y)

#Create list days and plot logistic curves
xall = list(range(0, 180))
y_fit = f(xall, a_, b_, c_, d_)
y_1pc = f(xall, a_, b_, c_, d_) * 0.01
y_3pc = f(xall, a_, b_, c_, d_) * 0.03
y_5pc = f(xall, a_, b_, c_, d_) * 0.05
y_7pc = f(xall, a_, b_, c_, d_) * 0.07

#Labels for the graph

sick = "w/{3} day sustained growth\ndue to incubation\nInitial Growth Rate: {0}%\nQuarantine GR: {1}%\nSick: {2:n}".format(round((phase1_gr-1)*100), round((phase2_gr-1)*100), int(round(f(xall[-1], a_, b_, c_, d_))), phase1)
Tsick = AnchoredText(sick, loc=2)
pc1357 = "Deaths Rates:\n7.0%: {3:n}\n5.0%: {2:n}\n3.0%: {1:n}\n1.0%: {0:n}\n0.1%: {4:n}".format(int(round(f(xall[-1], a_, b_, c_, d_) * 0.01, 0)),
                                                     int(round(f(xall[-1], a_, b_, c_, d_) * 0.03, 0)),
                                                     int(round(f(xall[-1], a_, b_, c_, d_) * 0.05, 0)),
                                                     int(round(f(xall[-1], a_, b_, c_, d_) * 0.07, 0)),
                                                     int(round(f(xall[-1], a_, b_, c_, d_) * 0.001, 0)))
Tpc = AnchoredText(pc1357, loc=5)

#Plot datapoints, curves, and labels
fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.ticklabel_format(style='plain', useOffset=False)
ax.add_artist(Tsick)
ax.add_artist(Tpc)
ax.plot(x, y, 'o')
ax.plot(x_orig, y_orig, 'ro')
ax.plot(xall, y_fit, '-')
ax.plot(xall, y_1pc, '-')
ax.plot(xall, y_3pc, '-')
ax.plot(xall, y_5pc, '-')
ax.plot(xall, y_7pc, 'r-')
plt.show()

