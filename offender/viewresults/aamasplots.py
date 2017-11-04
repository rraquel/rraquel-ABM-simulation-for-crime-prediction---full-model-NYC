import numpy as np
import matplotlib.pyplot as plt

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

#plt.figure(1)
#plt.subplot(211)
#plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
#plt.plot(t1, np.sin(2*np.pi*t1), 'b-*')
#plt.show()

"""plot unique crime hit rate vs. num of agent per strategy"""
#all cirmes
#select "uniqPai" from open.res_la_model where run_id=82 and step=1
#burlgary

#robbery

#larceny

#larcenyM

#assault
pai=np.array([0.7772844576245151,
0.7932475234033772,
0.6458019058472279,
0.6471939656370173,
0.7264492069656704,
0.7394903972587629,
0.6326098587831829])
agents=np.array([50,
50,
100,
50,
100,
100,
50])
plt.figure(1)
plt.subplot(211)
plot1=plt.plot(pai, agents,'-r')
plt.axis([0,200,0,1])
#plt.legend([plot1, plot2, plot3, plot4, plot4, plot5, plot6], ('randomRoad','randomRoadCenter', 'randomVenueCenter', 'randomVenue', 'popularVenue', 'popularVenueCenter'),'best' numpoints=1)
#patch1 = mpatches.Patch(color='red', label='randomroad')
#patch2 = mpatches.Patch(color='blue', label='randomRoadCenter')
#patch3 = mpatches.Patch(color='yellow', label='randomVenueCenter')
#patch4 = mpatches.Patch(color='green', label='randomVenue')
#patch5 = mpatches.Patch(color='cyan', label='popularVenue')
#patch6 = mpatches.Patch(color='magenta', label='popularVenueCenter')
#plt.legend(handles=[patch1, patch2, patch3, patch4, patch5, patch6], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#       ncol=2, mode="expand", borderaxespad=0.)
plt.show()
