import numpy as np
import matplotlib.pyplot as plt
import time
plt.figure(1)
a1=plt.subplot(211)
plt.ion()
for i in range(100):
    x=[i/10,(i+1)/10]
    x=np.array(x)
    y=np.sin(x)
    plt.plot(x,y)
    plt.pause(0.03)
    time.sleep(0.1)
    
    
