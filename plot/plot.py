import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
matplotlib.style.use('ggplot')


df = pd.read_csv('~/Documents/testout.log', sep=' ', header=None)
df.values

# array([[ 1. ,  2. ,  3. ],
#        [ 4. ,  5.5,  6. ]])
#
# # evenly sampled time at 200ms intervals
# t = np.arange(0., 5., 0.2)
# # print(t)
#
# plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'b--')
# plt.ylabel('some numbers')
# plt.savefig("test.svg")
# plt.show()


# import matplotlib.pyplot as plt
# import numpy as np
#
# plt.figure(figsize=[6,6])
# x = np.arange(0,100,0.00001)
# y = x*np.sin(2*pi*x)
# plt.plot(y)
# plt.axis('off')
# plt.gca().set_position([0, 0, 1, 1])
