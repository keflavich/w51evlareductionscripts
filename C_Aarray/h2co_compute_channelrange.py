rest = 4829.66*u.MHz
firstchan = (((35*u.km/u.s).to(u.MHz, u.doppler_radio(rest)) - 4824.861*u.MHz) / (7.812*u.kHz)).decompose()
lastchan = (((80*u.km/u.s).to(u.MHz, u.doppler_radio(rest)) - 4824.861*u.MHz) / (7.812*u.kHz)).decompose()
print firstchan, lastchan
