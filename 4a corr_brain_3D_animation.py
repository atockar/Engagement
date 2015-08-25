# Necessary for MacOSX
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



FLOOR = 0
CEILING = 60

class AnimatedScatter(object):
    def __init__(self):
        
        self.angle = 0

        brain_file = 'Data/Corr_brain.csv'
        self.brain = np.recfromcsv(brain_file, delimiter=',')
        self.time = self.brain.dtype.names[3]
        self.brain.sort(order=self.time)

        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('draw_event',self.forceUpdate)
        self.ax = self.fig.add_subplot(111,projection = '3d')
        # 601 actual frames from the data set
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=50, 
                                       init_func=self.setup_plot, blit=True,frames=700)


    # def change_angle(self):
    #     self.angle = (self.angle + 1)%360

    def forceUpdate(self, event):
        self.scat.changed()

    def setup_plot(self):
        # X = next(self.stream)
        X = np.zeros((1,3))

        corr = self.brain.dtype.names[5]
        # corrSet = list(set(self.brain[corr]))
        corrSet = self.brain[corr]
        # c = ['b', 'r', 'g', 'y', 'm']
        # c = [0.1,0.2,0.3,10,2]
        # c = corrSet
        # self.scat = self.ax.scatter(X[:,0], X[:,1], X[:,2] , c=c, cmap=plt.cm.YlOrRd_r, s=20, alpha=0.5, animated=True)
        self.scat = self.ax.scatter(X[:,0], X[:,1], X[:,2] , cmap=plt.cm.YlOrRd_r, s=20, alpha=0.5, animated=True)

        self.ax.set_xlim3d(FLOOR, CEILING)
        self.ax.set_ylim3d(FLOOR, CEILING)
        self.ax.set_zlim3d(FLOOR, CEILING)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        return self.scat,


    def update(self, i):

        brain_subset_idx = np.where(self.brain[self.time] == i)[0]
        brain_subset = self.brain[brain_subset_idx]

        x = self.brain.dtype.names[0]
        xArray = brain_subset[x]

        y = self.brain.dtype.names[1]
        yArray = brain_subset[y]

        z = self.brain.dtype.names[2]
        zArray = brain_subset[z]

        corr = self.brain.dtype.names[5]
        corrArray = brain_subset[corr]


        self.scat._offsets3d = ( np.ma.ravel(xArray) , np.ma.ravel(yArray) , np.ma.ravel(zArray) )
        self.scat._sizes = np.exp(corrArray * 8)
        # self.scat._sizes = np.exp((corrArray+1) * 3)
        # self.scat.set_array(np.ma.ravel(corrArray))
        # self.scat.set_array(corrArray)
        # self.scat.set_color(np.ma.ravel(corrArray))
        # self.scat._array(corrArray)
        # self.scat.autoscale()
        # self.scat.cmap(plt.cm.YlOrRd_r)

        plt.draw()
        return self.scat,

    def show(self):
        plt.show()

    def save(self, fileDir):
        self.ani.save(fileDir, fps=30, extra_args=['-vcodec', 'libx264'])

if __name__ == '__main__':
    a = AnimatedScatter()
    # a.save('final_animation.mp4')
    a.show()








