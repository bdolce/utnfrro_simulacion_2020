import matplotlib.pyplot as plt
import numpy as np

n = np.random.normal(0.49979683229902605, 0.0903745152449981,100000)

count, bins, ignored = plt.hist(n, 30, density=True)
plt.hist(n,bins,linewidth=2, color='r')
plt.show()
