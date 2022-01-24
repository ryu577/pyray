"""
A point-swarm is a kind of shape (or lack thereof).
Different ways to move a large number of points
and make them do various things.
"""

import numpy as np
from pyray.rotation import *
from PIL import Image, ImageDraw, ImageFont, ImageMath


def drip_to_bins(draw, xs, m, t, r, 
				rgb=(20,255,102), 
				transparency=120, 
				trp_hi=120, 
				trp_lo=120,
				lo_ind=0,
				hi_ind=1000,
				xshift=0):
	"""
	Make some points fall down into bins.
	"""
	w = 5
	
	hts = np.zeros(len(xs)+1)
	#https://stackoverflow.com/a/2828121/1826912
	m = m[m[:,1].argsort()[::-1]]
	for i in range(m.shape[0]):
		r_pt = generalized_planar_rotation(m[i], np.array([1000,1000]), r)      
		x = r_pt[0]
		y = r_pt[1] + t*10
		for j in range(1,len(xs)):
			if xs[j-1] < x and x < xs[j]:
				base_y = 2040 - hts[j-1]*10
				if y > base_y+10:
					if j > hi_ind:
						rgba = rgb + (trp_hi,)
					elif j < lo_ind:
						rgba = rgb + (trp_lo,)
					else:
						rgba = rgb + (transparency,)
					draw.polygon([(xs[j-1]+xshift, base_y),(xs[j]+xshift, base_y),(xs[j]+xshift, base_y-10),(xs[j-1]+xshift, base_y-10)],fill=rgba)
					hts[j-1] += 1
				else:
					x = x+xshift
					draw.ellipse((x-w,y-w,x+w,y+w), fill=rgb, outline = (0,0,0)) 


def binary_classificn_pts(extent=0, datt=[], scale=1, r=np.eye(2), t1=0, t2=0, 
						  trnsp1=120, trnsp2=120,
						  trp1_hi=120, trp1_lo=120,
						  trp2_hi=120, trp2_lo=120,
						  hi1_ind=1000, lo1_ind=0,
						  hi2_ind=1000, lo2_ind=0,
						  xshift1=0, xshift2=0):
	# Basic stuff with points.
	w=5
	im = Image.new("RGB", (2048, 2048), (1, 1, 1))
	draw = ImageDraw.Draw(im, 'RGBA')
	if extent == 0:
		return (im, draw)
	means1_orig = np.array([500, 1500])
	means2_orig = np.array([1500, 500])

	means1 = generalized_planar_rotation(means1_orig, np.array([1000,1000]), r)
	means2 = generalized_planar_rotation(means2_orig, np.array([1000,1000]), r)
	p=0.3
	center_1_orig = means1_orig*p+means2_orig*(1-p)
	center_2_orig = means2_orig*p+means1_orig*(1-p)
	center_1 = means1*p+means2*(1-p)
	center_2 = means2*p+means1*(1-p)
	means = center_1
	stds = [300, 300]
	corr = 0.8         # correlation
	covs = [[stds[0]**2          , stds[0]*stds[1]*corr],
			[stds[0]*stds[1]*corr,           stds[1]**2]]
	np.random.seed(0)
	m_1 = np.random.multivariate_normal(center_1_orig, covs, 200)*scale
	m = m_1
	for i in range(m.shape[0]):
		r_pt = generalized_planar_rotation(m[i], np.array([1000,1000]), r)
		if extent > 0 and extent < 5:
			draw.ellipse((r_pt[0]-w,r_pt[1]-w,r_pt[0]+w,r_pt[1]+w), fill = (255,30,102), outline = (0,0,0))
	means = center_2
	np.random.seed(4)
	m_2 = np.random.multivariate_normal(center_2_orig, covs, 200)*scale
	m = m_2
	for i in range(m.shape[0]):
		r_pt = generalized_planar_rotation(m[i], np.array([1000,1000]), r)
		if extent > 1 and extent < 5:
			draw.ellipse((r_pt[0]-w,r_pt[1]-w,r_pt[0]+w,r_pt[1]+w), fill = (20,255,102), outline = (0,0,0))
	
	# Draw the separating line.
	center = (center_1+center_2)/2
	orthog = -np.dot(planar_rotation(-np.pi/2), (center_2-center_1))
	main_dircn = (center_2 - center_1)
	p=2.0
	pt_1 = center + orthog*p
	pt_2 = center - orthog*p
	if extent > 2:
		draw.line((pt_1[0], pt_1[1], pt_2[0], pt_2[1]), fill = 'grey', width = 7)

	avgs = []
	means = np.sum(m_1,axis=1)/2
	avgs2 = []
	means2 = np.sum(m_2,axis=1)/2
	for i in range(len(means)):
		avgs.append((((m_1[i][1]<m_1[i][0]))-0.5)*2*np.sqrt(sum((m_1[i]-means[i])**2)))
		avgs2.append((((m_2[i][1]<m_2[i][0]))-0.5)*2*np.sqrt(sum((m_2[i]-means2[i])**2)))
	avgs = np.array(avgs)
	avgs2 = np.array(avgs2)
	dat1 = m_1[avgs > np.percentile(avgs,97)]
	dat2 = m_2[avgs2 < np.percentile(avgs,4)]
	for i in dat1:
		datt.append(i)
	for i in dat2:
		datt.append(i)
	xs = [1000]
	for i in range(1,8):
		pt_1_a = pt_1 + main_dircn*i/7
		pt_1_b = pt_1 - main_dircn*i/7
		pt_2_a = pt_2 + main_dircn*i/7
		pt_2_b = pt_2 - main_dircn*i/7
		if extent > 3:
			draw.line((pt_1_a[0], pt_1_a[1], pt_2_a[0], pt_2_a[1]), fill = (255,255,255,100), width = 4)
			draw.line((pt_1_b[0], pt_1_b[1], pt_2_b[0], pt_2_b[1]), fill = (255,255,255,100), width = 4)
		xs.append(pt_1_a[0])
		xs.append(pt_1_b[0])
	xs.sort()
	xs.append(max(xs)+xs[1]-xs[0])
	xs.append(min(xs)-xs[1]+xs[0])
	# I basically want to transfer the last element to the first position
	# so sort is overkill. But it's a small array, so no matter.
	xs.sort()
	if extent > 4:
		drip_to_bins(draw, xs, m, t1, r, rgb=(20,255,102), transparency=trnsp1, trp_hi=trp1_hi, trp_lo=trp1_lo,
			hi_ind=hi1_ind,lo_ind=lo1_ind,xshift=xshift1)
		drip_to_bins(draw, xs, m_1, t2, r, rgb=(255,20,102), transparency=trnsp2, trp_hi=trp2_hi, trp_lo=trp2_lo,
			hi_ind=hi2_ind,lo_ind=lo2_ind,xshift=xshift2)
	return (im, draw)



def points_to_bins():
	(im, draw) = make_again(1, dd1, r=planar_rotation(0))
	im.save("..\\images\\RotatingCube\\im" + str(int(0)) + ".png")
	im.save("..\\images\\RotatingCube\\im" + str(int(1)) + ".png")
	im.save("..\\images\\RotatingCube\\im" + str(int(2)) + ".png")

	im.close()
	for i in range(3,14):
		(im, draw) = make_again(1, dd1, r=planar_rotation(-np.pi/4*(i-3)/10))
		im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")


	base = i
	im.close()
	ind = 0
	for t in range(180):
		if t%5==0:
			(im, draw) = make_again(2, dd1, r=planar_rotation(-np.pi/4), t1=t)
			im.save("..\\images\\RotatingCube\\im" + str(int(base+ind)) + ".png")
			ind+=1

	base = base + ind
	im.close()
	ind=0
	for t in range(185):
		if t%5==0:
			(im, draw) = make_again(2, dd1, r=planar_rotation(-np.pi/4), t1=180, t2=t)
			im.save("..\\images\\RotatingCube\\im" + str(int(base+ind)) + ".png")
			ind+=1


def make_again(extent=0, datt=[], scale=1, r=np.eye(2), t1=0, t2=0):
    # Basic stuff with points.
    w=5
    im = Image.new("RGB", (2048, 2048), (1, 1, 1))
    draw = ImageDraw.Draw(im, 'RGBA')
    means1_orig = np.array([500, 1500])
    means2_orig = np.array([1500, 500])

    means1 = generalized_planar_rotation(means1_orig, np.array([1000,1000]), r)
    means2 = generalized_planar_rotation(means2_orig, np.array([1000,1000]), r)
    p=0.3
    center_1_orig = means1_orig*p+means2_orig*(1-p)
    center_2_orig = means2_orig*p+means1_orig*(1-p)
    center_1 = means1*p+means2*(1-p)
    center_2 = means2*p+means1*(1-p)
    means = center_1
    stds = [300, 300]
    corr = 0.8         # correlation
    covs = [[stds[0]**2          , stds[0]*stds[1]*corr], 
            [stds[0]*stds[1]*corr,           stds[1]**2]] 
    np.random.seed(0)
    m_1 = np.random.multivariate_normal(center_1_orig, covs, 200)*scale
    m = m_1
    for i in range(m.shape[0]):
        r_pt = generalized_planar_rotation(m[i], np.array([1000,1000]), r)
        if extent < 2:
            draw.ellipse((r_pt[0]-w,r_pt[1]-w,r_pt[0]+w,r_pt[1]+w), fill = (255,255,102), outline = (0,0,0))
    means = center_2
    np.random.seed(4)
    m_2 = np.random.multivariate_normal(center_2_orig, covs, 200)*scale
    m = m_2
    for i in range(m.shape[0]):
        r_pt = generalized_planar_rotation(m[i], np.array([1000,1000]), r)
        if extent < 2:
            draw.ellipse((r_pt[0]-w,r_pt[1]-w,r_pt[0]+w,r_pt[1]+w), fill = (20,255,102), outline = (0,0,0))

    if extent > 0:
        # Draw the separating line.
        center = (center_1+center_2)/2
        orthog = -np.dot(planar_rotation(-np.pi/2), (center_2-center_1))
        main_dircn = (center_2 - center_1)
        p=2.0
        pt_1 = center + orthog*p
        pt_2 = center - orthog*p
        draw.line((pt_1[0], pt_1[1], pt_2[0], pt_2[1]), fill = 'orange', width = 7)

    avgs = []
    means = np.sum(m_1,axis=1)/2
    for i in range(len(means)):
        avgs.append( (((m_1[i][1]<m_1[i][0]))-0.5)*2*np.sqrt(sum((m_1[i]-means[i])**2)))
    avgs = np.array(avgs)
    dat1 = m_1[avgs > np.percentile(avgs,97)]
    for i in dat1:
        datt.append(i)
    xs = [1000]
    for i in range(1,8):
        pt_1_a = pt_1 + main_dircn*i/7
        pt_1_b = pt_1 - main_dircn*i/7
        pt_2_a = pt_2 + main_dircn*i/7
        pt_2_b = pt_2 - main_dircn*i/7
        draw.line((pt_1_a[0], pt_1_a[1], pt_2_a[0], pt_2_a[1]), fill = (255,255,255,100), width = 4)
        draw.line((pt_1_b[0], pt_1_b[1], pt_2_b[0], pt_2_b[1]), fill = (255,255,255,100), width = 4)
        xs.append(pt_1_a[0])
        xs.append(pt_1_b[0])
    xs.sort()
    xs.append(max(xs)+xs[1]-xs[0])
    xs.append(min(xs)-xs[1]+xs[0])
    # I basically want to transfer the last element to the first position
    # so sort is overkill. But it's a small array, so no matter.
    xs.sort()
    if extent >=2:
        drip_to_bins(draw, xs, m, t1, rgb=(20,255,102))
        drip_to_bins(draw, xs, m_1, t2, rgb=(255,255,102))
    return (im, draw)


