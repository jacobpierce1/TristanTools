import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# fig, ax = plt.subplots()
# xdata, ydata = [], []
# ln, = ax.plot([], [], '-', color = 'g' )

# def init():
#     ax.set_xlim(0, 2*np.pi)
#     ax.set_ylim(-1, 1)
#     return ln,

# def update(frame):
#     xdata.append(frame)
#     ydata.append(np.sin(frame))
#     ln.set_data(xdata, ydata)
#     return ln,

# ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                     init_func=init, blit=True)
# plt.show()



fig, ax = plt.subplots()

# y = np.arange(3, dtype = float )
# y[2] = np.nan

# ax.plot( np.arange(3), y )

ndata = 1000

tmp = np.zeros( ( ndata, ndata ) ) 

tmp[0] = np.random.normal( 0, 1, ndata ) 

for i in range( 1, ndata ) :
    tmp[i] = tmp[i-1] + np.random.normal( 0, 0.02, ndata ) 


x = np.arange( ndata )

for i in range( ndata) :
    line = ax.plot( x, tmp[:,i], c = 'k', linewidth = 0.01 )
    # line.alpha = 0.1 
    

plt.show()
