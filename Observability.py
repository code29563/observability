# -*- coding: utf-8 -*-

#code to check when an object is observable

import astropy
import astroplan
import dateutil

constraint = [astroplan.AltitudeConstraint(30*astropy.units.deg)] #constraints that must be fulfilled for the target to be observable

Observer = astroplan.Observer(longitude=astropy.coordinates.Angle('3d11m16sW'), latitude=astropy.coordinates.Angle('55d55m23sN'),elevation=146*astropy.units.m)

coord = astropy.coordinates.SkyCoord('10 17 09.6 +39 01 00', unit=(astropy.units.hourangle, astropy.units.deg),equinox='J2000') #RA and DEC coordinates of object

target = astroplan.FixedTarget(coord) #making a target object for the target

interval = 5
p = dateutil.rrule.rrule(dateutil.rrule.MINUTELY,dateutil.parser.parse('2021-01-23 20:00'),interval=interval,until=dateutil.parser.parse('2021-03-27 12:00'),byhour=[16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8]) #the time every 5 minutes from '2021-01-23 20:00' until '2021-01-30', only in the specified hours
#print(list(p))

d = 0 #initiating the value of d

for t in p: #iterating through the times
    time = astropy.time.Time(t) #UTC by default I think
    a = astroplan.is_event_observable(constraint,Observer,target,time)
    if a[0][0]==True: #i.e. if the target is observable
        if d==0: #if the previous check showed the target is not observable (or this is the first iteration)
            d = 1
            print(t,end=',') #printing when the target is observable from, which is the first value that's true
    else: #i.e. if the target is not observable; alternatively use: elif str(a[0][0])=='False'
        if d==1: #if the previous check showed the target is observable
            d = 0
            print(t-dateutil.relativedelta.relativedelta(minutes=interval)) #printing when the target is observable until, which is the last value that was true; 'minutes' because MINUTELY was used above, and 'interval' because that was the interval above
