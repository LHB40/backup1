import numpy as np
import matplotlib.pyplot as plt
import time

plt.figure(1) # 创建图表1
ax1 = plt.subplot(311) # 在图表2中创建子图1
ax2 = plt.subplot(212) # 在图表2中创建子图2
x = np.linspace(0, 3, 100)
for i in  range(5):
    plt.sca(ax1)   #选择图表2的子图1
    plt.plot(x, np.sin(i*x))
    plt.sca(ax2)  # 选择图表2的子图2
    plt.plot(x, np.cos(i*x))
    plt.xlim(-0.1,3.1)
    plt.xlabel('A ')
plt.show()
 
