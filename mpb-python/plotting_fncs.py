import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plot3D_epsilon(dLoc, npce):
    #takes numpy array of 3D matrix of dielectric values
    zlen = len(npce[0,0,:])
    ylen = len(npce[0,:,0])
    xlen = len(npce[:,0,0])

    xs, ys = np.meshgrid(np.arange(0,xlen), np.arange(0,ylen))
    xs, ys, zs = np.meshgrid(np.arange(0,ylen), np.arange(0,xlen), np.arange(0,zlen))

    xsf = xs.flatten()
    ysf = ys.flatten()
    zsf = zs.flatten()
    npcef = npce.flatten()

    xsf = xsf[npcef > 1]
    ysf = ysf[npcef > 1]
    zsf = zsf[npcef > 1]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.scatter(xsf, ysf, zsf)
    plt.xlabel('y axis index') 
    plt.ylabel('x axis index')
    ax.set_xlim3d(0,ylen)
    ax.set_ylim3d(0,xlen)
    ax.set_zlim3d(0,zlen)
    plt.savefig(dLoc + '3Dplot.png')

    plt.show()


def plot_2Dslice_epsilon(dLoc, npce, coord):

	###plot geom
	zlen = len(npce[0,0,:])
	ylen = len(npce[0,:,0])
	xlen = len(npce[:,0,0])

	zslice = npce[:,:,round(zlen/2)]

	plt.imshow(zslice, interpolation='spline36', cmap='binary')


	plt.title('Refractive index slice through z = 0')
	plt.xlabel('x ')
	plt.ylabel('y ')
	plt.savefig(dLoc + '2Dzslice.png')
	plt.show()

	plt.close()

def plot_bands(dLoc, te_freqs, te_gaps, tm_freqs, tm_gaps, freqscale):
	##plot bands
	#input freqscale = 1 for units of c/a

	te_freqs = te_freqs*freqscale
	tm_freqs = tm_freqs*freqscale

	fig, ax = plt.subplots()
	x = range(len(tm_freqs))
	x = x/np.amax(x)*0.5
	# Plot bands
	# Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
	for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
	    ax.scatter([xz]*len(tmz), tmz, color='blue')
	    ax.scatter([xz]*len(tez), tez, color='red', facecolors='none')
	ax.plot(x,tm_freqs, color='blue')
	ax.plot(x,te_freqs, color='red')
	ax.set_xlim([x[0], x[-1]])

	# Plot gaps
	for gap in tm_gaps:
		print(gap[0])
		print('was gap0')
		if gap[0] > 1:
			ax.fill_between(x, gap[1]*freqscale, gap[2]*freqscale, color='blue', alpha=0.2)

	for gap in te_gaps:
	    if gap[0] > 1:
	        ax.fill_between(x, gap[1]*freqscale, gap[2]*freqscale, color='red', alpha=0.2)


	# Plot labels
	ax.text(12, 0.04, 'TM bands', color='blue', size=15)
	ax.text(13.05, 0.235, 'TE bands', color='red', size=15)


	#light line is given by c*ky*(2pi/period)/2pi/n_air 
	#frequencies are already outputted in terms of c/a
	#so light line is just (c/a)*k_y; but c/a =1 

	ax.plot(x, x*freqscale, color='black') 

	if freqscale == 1:
		ax.set_ylabel('frequency (c/a)', size=16)
	else:
		ax.set_ylabel('frequency (THz)', size=16)

	ax.set_xlabel('kpoint ($k_x\cdot a/2 \pi$)')
	ax.grid(True)
	plt.savefig(dLoc + 'mpbbands.png')

	plt.show()

def save_bands(dLoc, te_freqs, te_gaps, tm_freqs, tm_gaps, freqscale):
	tefLoc = dLoc + 'normalized_tefreqs.txt'
	#tegLoc = dLoc + 'normalized_tegaps.txt'
	tmfLoc = dLoc + 'normalized_tmfreqs.txt'
	#tmgLoc = dLoc + 'normalized_tmgaps.txt'


	np.savetxt(tefLoc, te_freqs*freqscale)
	np.savetxt(tmfLoc, tm_freqs*freqscale)
