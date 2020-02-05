from sky.models import Direction, SkyObject

d = Direction(epoch='J2000', ra='05h34m32s', dec='+22d00m52s')
d.save()
SkyObject(name='Tau A', direction=d).save()

d = Direction(epoch='J2000', ra='12h30m49s', dec='+12d23m28s')
d.save()
SkyObject(name='Vir A', direction=d).save()

d = Direction(epoch='J2000', ra='19h59m29s', dec='+40d44m02s')
d.save()
SkyObject(name='Cyg A', direction=d).save()

d = Direction(epoch='J2000', ra='23h23m24s', dec='+58d48m54s')
d.save()
SkyObject(name='Cas A', direction=d).save()

d = Direction(epoch='J2000', ra='16h51m11s', dec='+05d04m58s')
d.save()
SkyObject(name='Herc A', direction=d).save()

d = Direction(epoch='J2000', ra='06h18m02.7s', dec='+22d39m36s')
d.save()
SkyObject(name='Gem A', direction=d).save()

d = Direction(epoch='J2000', ra='09h18m05.651s', dec='-12d05m43.99s')
d.save()
SkyObject(name='Hya A', direction=d).save()

SkyObject(name='Sun').save()
SkyObject(name='Jupiter').save()
SkyObject(name='Moon').save()
