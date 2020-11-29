#adapted from: 
#https://mpb.readthedocs.io/en/latest/Python_Data_Analysis_Tutorial/

import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from plotting_fncs import *
import os

num_bands = 4
kpt_resolution = 4 
resolution = 32

w_actual = 490e-9
a_actual = 261e-9
theta = 35 #in degrees
hx_actual = 103e-9
hy_actual = 390e-9

c = 299792458 #speed of light in m/s
n = 2.4063

#location to save text files in
paramstring = 'w-{:.0f}nm_a-{:.0f}nm_theta-{:.0f}deg_hx-{:.0f}nm_hy-{:.0f}nm_'.format(
    w_actual*10**9, a_actual*10**9, theta, hx_actual*10**9, hy_actual*10**9)
dFolder = '/Users/mvchalupnik/Desktop/mympbplots/'
dLoc = dFolder + paramstring
if not os.path.exists(dFolder):
    os.makedirs(dFolder)

w = w_actual/a_actual
a = 1
hx = hx_actual/a_actual
hy = hy_actual/a_actual
h = w/2/np.tan(theta*np.pi/180)


####################################################################

#sets size of lattice to be 3D; 1by1by1
geometry_lattice = mp.Lattice(size=mp.Vector3(a, w*3, h*3))

#https://meep.readthedocs.io/en/latest/Python_User_Interface/#prism
beam = mp.Prism([mp.Vector3(0,-w/2, h/2), mp.Vector3(0,w/2, h/2), mp.Vector3(0,0, -h/2)], a, axis=mp.Vector3(1,0,0), 
    center=None, material=mp.Medium(epsilon=n**2))
#Diamond: n = 2.4063; n^2 = ep_r


hole = mp.Ellipsoid(size=[hx, hy, mp.inf], material=mp.Medium(epsilon=1))

geometry = [beam, hole]

#Symmetry points
k_points = [
    mp.Vector3(0,0,0),               # Gamma
    mp.Vector3(0.5,0,0),          # X (normalized to a?)
]
#how many points to solve for between each specified point above
k_points = mp.interpolate(kpt_resolution, k_points) 

#geometry_center
#ModeSolver documentation: https://mpb.readthedocs.io/en/latest/Python_User_Interface/
ms = mpb.ModeSolver(
    geometry=geometry,
    geometry_lattice=geometry_lattice,
    k_points=k_points,
    resolution=resolution,
    num_bands=num_bands,
)

#https://mpb.readthedocs.io/en/latest/Python_User_Interface/
ms.run_yeven(mpb.output_at_kpoint(mp.Vector3(0.5,0,0), mpb.fix_efield_phase,
          mpb.output_efield_z)) #This will output the electric field at the xpoint only
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
ms.run_yodd()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list


###plot geom
md = mpb.MPBData(rectify=True, periods=1, resolution=resolution)
eps = ms.get_epsilon()
converted_eps = md.convert(eps)
print(np.shape(converted_eps))

np_converted_eps = np.array(converted_eps)


npce = np.array(converted_eps)

plot_2Dslice_epsilon(dLoc,npce,0)
plot3D_epsilon(dLoc,npce)


plot_bands(dLoc,te_freqs, te_gaps, tm_freqs, tm_gaps, c/a_actual*1e-12)
save_bands(dLoc,te_freqs, te_gaps, tm_freqs, tm_gaps,c/a_actual*1e-12)


