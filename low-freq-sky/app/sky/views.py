#!/usr/bin/env python

from django.http import HttpResponse
from sky import models
from django.shortcuts import render

from casacore.measures import measures
import math
import datetime as py_datetime
import json
import collections

import os
os.environ["HOME"] = "/low-freq-sky/app/home"

def direction_model2pyrap(me, d):
	"""Takes a casacore measures object and model Direction.
	Returns a casacore Direction"""
	return me.direction(str(d.epoch), str(d.ra), str(d.dec))

def skyObject2pyrap(me, s):
	"""Takes a casacore measures object and model SkyObject.
	Returns a casacore Direction"""
	if s.direction:
		return direction_model2pyrap(me, s.direction)
	else:
		return me.direction(s.name)

def galaxy_up(arr):
	"""arr is a list of points in the galactic plane
	   in AZ,EL. We need to output a single sequence
	   of points that are "up" (EL>0), removing
	   "set" (EL<0) points. Furthermore it needs to
	   be ordered horizon to horizon"""
	if not [i for i in arr if i['EL'] > 0]:
		# Galaxy below horizon
		return []
	g = collections.deque(arr)
	# Rotate past the initial "up" points
	while g[0]['EL'] > 0:
		g.rotate(1)
	# or wind back if we're in the "set" range
	while g[1]['EL'] < 0:
		g.rotate(-1)
	# remove the "set" points
	for i in range(len(g)-1, 0, -1):
		if g[i-1]['EL'] < 0:
			g.pop()
		else:
			break
	return list(g)

def sky_all(request, observatory, datetime, timezone, template_name):
	me = measures()
	if observatory == "ovro":
		obs_position = me.observatory("CARMA")
	elif observatory == "onsala":
		obs_position = me.observatory("OSO")
	elif observatory == "exloo":
		obs_position = me.observatory("LOFAR")
	elif observatory == "birr":
		obs_position = me.position("ITRF", "3801633.52806m", "-529021.899396m", "5076997.185m")
	elif observatory == "mwa":
		obs_position = me.observatory("MWA")
	elif observatory == "gmrt":
		obs_position = me.observatory("GMRT")
	else:
		obs_position = me.observatory("CARMA")

	dt_fmt = '%Y/%m/%d/%H:%M:%S'
	dt = py_datetime.datetime.strptime(datetime, dt_fmt)
	tz = py_datetime.timedelta(hours=int(timezone[:3]), minutes=int(timezone[3:]))
	time = me.epoch('UTC', (dt - tz).strftime(dt_fmt))

	# Set the position and epoch of the measures object
	me.do_frame(obs_position)
	me.do_frame(time)

	sources = []
	galaxy = []
	FLOAT_PRECISION = 5 # > arc-minute accuracy, limit to reduce JSON size.
	for src in models.SkyObject.objects.all():
		d_sky = skyObject2pyrap(me, src) # J2000 direction
		d_ground = me.measure(d_sky, 'AZEL') # Convert to AZ,EL
		az = d_ground['m0']['value']
		el = d_ground['m1']['value']
		info = {'Name':str(src.name), 'AZ': round(az, FLOAT_PRECISION), 'EL': round(el, FLOAT_PRECISION)}
		if src.name == 'gp':
			galaxy.append(info)
		else:
			sources.append(info)
	
	return HttpResponse(json.dumps({'sources': sources, 'galaxy': galaxy_up(galaxy)}))
