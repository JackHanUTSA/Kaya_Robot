from math import sqrt
import numpy as np 

L = 13.5 #13.5 centimerters
r = 0.4 #4cm
kaya_inv_kine = [[sqrt(3)/2, 1/2, L],
             [0, -1, L],
             [-sqrt(3)/2, 1/2, L]]


kaya_dir_kine = [[sqrt(3), 0, -sqrt(3)],
             [1, -2, 1],
             [1/L, 1/L, 1/L]]


ohmegas = 1/r *np.dot(kaya_inv_kine,dir_n)
