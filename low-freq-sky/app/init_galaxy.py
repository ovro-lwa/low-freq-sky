from sky.models import Direction, SkyObject
import math

POINTS = 48
for i in range(POINTS):
	d = Direction(epoch='GALACTIC', ra='%frad' % (i*2*math.pi/POINTS), dec='0rad')
	d.save()
	SkyObject(name='gp', direction=d).save()
