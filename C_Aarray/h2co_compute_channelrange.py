from astropy import units as u
rest = 4829.66*u.MHz
chwid = (7.8125*u.kHz)
chan0 = 4824.861*u.MHz
vlsr = 42.27*u.km/u.s
firstchan = (((35*u.km/u.s-vlsr).to(u.MHz, u.doppler_radio(rest)) - chan0) / chwid).decompose()
lastchan = (((80*u.km/u.s-vlsr).to(u.MHz, u.doppler_radio(rest)) - chan0) / chwid).decompose()
print firstchan, lastchan
print "Frequency at channel 550: ",(550*chwid + chan0).to(u.GHz)
print "Frequency at channel 0: ",(0*chwid + chan0).to(u.GHz)
print "Frequency at channel 1024: ",(1024*chwid + chan0).to(u.GHz)
print "Frequency at channel 512: ",(512*chwid + chan0).to(u.GHz)," and according to CASA: ",4.82886*u.GHz
print "total bw: ",1024*chwid
