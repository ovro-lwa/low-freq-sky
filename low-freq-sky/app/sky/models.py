from django.db import models

class Direction(models.Model):
	epoch = models.CharField(max_length=10)
	ra = models.CharField(max_length=15)
	dec = models.CharField(max_length=15)

	def __unicode__(self):
        	return u'%s %s %s' % (self.epoch, self.ra, self.dec)

class SkyObject(models.Model):
	name = models.CharField(max_length=20)
	direction = models.ForeignKey(Direction, blank=True, null=True, on_delete=models.SET_NULL)

	def __unicode__(self):
		return self.name
