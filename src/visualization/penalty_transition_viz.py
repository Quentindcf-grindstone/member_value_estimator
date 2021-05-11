import numpy as np
from matplotlib import pyplot as plt

X_array = np.linspace(0,0.35,351)
print(X_array)

def fraud_pen(x, transition_stage):
    if x < 0.08:
        return 0
    elif x < 0.1:
        return 2*x*transition_stage
    else:
        return 3*x*transition_stage

def new_fp(x, transition_stage):
    return transition_stage*(np.arctan(25*x - 2)* (2/np.pi)*1.25)

Y_current = np.ones(351)
Y_transition = np.ones(351)
X_forDotLine = np.linspace(0,0.35,18)
Y_forDotLine = np.linspace(0,1,50)
Y_1 = np.ones(18)
Y_0 = np.zeros(18)
X_025 = np.ones(50)/4
X_010 = np.ones(50)/10

for i in range(len(X_array)):
    Y_current[i] = 1 - fraud_pen(X_array[i], 1 ) - new_fp(X_array[i], 0)
    Y_transition[i] = 1 - new_fp(X_array[i],  1)
# plt.plot(X_array,Y_current)
# plt.legend(['current'])
# plt.show()

plt.plot(X_array,Y_current)
plt.plot(X_array,Y_transition)
plt.hlines(1, 0, 0.35, linestyles='dotted')
plt.hlines(0, 0, 0.35, linestyles='dotted')
plt.vlines(0.10, -0.25, 1.25, linestyles='dotted')
plt.vlines(0.25, -0.25, 1.25, linestyles='dotted')
plt.legend(['before', 'after'])
plt.yticks(np.linspace(-0.25,2,10))
plt.show()

# for k in range(5):
#     for i in range(len(X_array)):
#         Y_current[i] = 1 - fraud_pen(X_array[i], 1 - 0.2*k) - new_fp(X_array[i], 0.2*k)
#         Y_transition[i] = 1 - fraud_pen(X_array[i], 1 - 0.2*(k+1)) - new_fp(X_array[i],  0.2*(k+1))
#     plt.plot(X_array,Y_current)
#     plt.plot(X_array,Y_transition)
#     plt.legend( ['before', 'after'])
#     plt.show()



