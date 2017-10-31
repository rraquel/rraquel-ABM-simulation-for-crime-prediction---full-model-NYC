import numpy as np
import matplotlib.pyplot as plt

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.figure(1)
plt.subplot(211)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.plot(t1, np.sin(2*np.pi*t1), 'b-*')
plt.show()

"""plot unique crime hit rate vs. num of agent per strategy"""
#all cirmes
#select "uniqPai" from open.res_la_model where run_id=82 and step=1
#burlgary

#robbery

#larceny

#larcenyM

#assault
