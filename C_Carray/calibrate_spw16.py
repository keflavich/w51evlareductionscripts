"""
Calibration following https://casaguides.nrao.edu/index.php?title=EVLA_6cmWideband_Tutorial_SN2010FZ
"""

vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
spw16vis='CbandCarray_spw16_raw_continuum.ms'
refant = 'ea14'
fluxcal = '0137+331=3C48'
phasecal = 'J1922+1530'
source = 'W51 Ku'
spwrange = "0:10~118"

split(vis=vis, outputvis=spw16vis, datacolumn='data', spw='16')

imagename = 'CbandCarray_spw16_raw_continuum_nocal_dirty'
clean(vis=spw16vis,
      imagename=imagename,
      field=source,
      weighting='briggs', imsize=[256,256], cell=['1.0 arcsec'],
      mode='mfs', threshold='20 mJy', niter=0,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)

setjy_dict = setjy(vis=spw16vis, field=fluxcal, scalebychan=True, model='3C48_C.im',
                   usescratch=False, standard='Perley-Butler 2013')
print('setjy: ', setjy_dict)

rmtables(['cal_spw16.G0','cal_spw16.K0','cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.G1inf'])
gencal(vis=spw16vis,caltable='cal_spw16.antpos',caltype='antpos',antenna='')
gencal(vis=spw16vis,caltable='cal_spw16.gaincurve',caltype='gc')
# not needed for 8bit gencal(vis=spw16vis,caltable='cal_spw16.requantizer',caltype='rq')
gaincal(vis=spw16vis,caltable='cal_spw16.G0', field=fluxcal,spw=spwrange,
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve'],
        gaintype='G',refant=refant,calmode='p',solint='int',minsnr=3)

gaincal(vis=spw16vis,caltable='cal_spw16.K0',
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.G0'],
        field=fluxcal,spw=spwrange,gaintype='K',
        refant=refant,combine='scan',solint='inf',minsnr=3)

bandpass(vis=spw16vis,caltable='cal_spw16.B0',
         gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                    'cal_spw16.G0','cal_spw16.K0'],
         field=fluxcal,refant=refant,solnorm=False,
         bandtype='B', combine='scan', solint='inf')

gaincal(vis=spw16vis,caltable='cal_spw16.G1int', \
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                   'cal_spw16.K0','cal_spw16.B0'], \
        field=fluxcal,refant=refant,solnorm=False, \
        spw=spwrange, \
        solint='int',gaintype='G',calmode='p')

gaincal(vis=spw16vis,caltable='cal_spw16.G1int', \
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                   'cal_spw16.K0','cal_spw16.B0'], \
        field=phasecal,refant=refant,solnorm=False, \
        spw=spwrange,
        solint='int',gaintype='G',calmode='p',append=True)


gaincal(vis=spw16vis,caltable='cal_spw16.G1inf',
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                   'cal_spw16.K0','cal_spw16.B0'], \
        field=phasecal,refant='ea04',solnorm=F, \
        spw=spwrange, \
        solint='inf',gaintype='G',calmode='p')

gaincal(vis=spw16vis, caltable='cal_spw16.G2', \
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                   'cal_spw16.K0','cal_spw16.B0','cal_spw16.G1int'], \
        gainfield=['','',fluxcal,fluxcal,fluxcal], \
        interp=['','','nearest','nearest','nearest'], \
        field=fluxcal,refant='ea04',solnorm=F,
        spw=spwrange, \
        solint='inf',combine='scan',gaintype='G',calmode='a')
#
gaincal(vis=spw16vis, caltable='cal_spw16.G2', \
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                   'cal_spw16.K0','cal_spw16.B0','cal_spw16.G1int'],\
        gainfield=['','',fluxcal,fluxcal,phasecal], \
        interp=['','','nearest','nearest','nearest'], \
        field=phasecal,refant='ea04',solnorm=F, \
        spw=spwrange, \
        solint='inf',gaintype='G',calmode='a',append=True)


gaincal(vis=spw16vis, caltable='cal_spw16.G3', \
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                   'cal_spw16.K0','cal_spw16.B0','cal_spw16.G1int'], \
        gainfield=['','',fluxcal,fluxcal,fluxcal], \
        interp=['','','nearest','nearest','nearest'], \
        field=fluxcal,refant='ea04',solnorm=F,
        spw=spwrange, \
        solint='inf',combine='scan',gaintype='G',calmode='a')
#
gaincal(vis=spw16vis, caltable='cal_spw16.G3', \
        gaintable=['cal_spw16.antpos','cal_spw16.gaincurve',
                   'cal_spw16.K0','cal_spw16.B0','cal_spw16.G1int'],\
        gainfield=['','',fluxcal,fluxcal,phasecal], \
        interp=['','','nearest','nearest','nearest'], \
        field=phasecal,refant='ea04',solnorm=F, \
        spw=spwrange, \
        solint='inf',combine='scan',gaintype='G',calmode='a',append=True)

myflux = fluxscale(vis=spw16vis,caltable='cal_spw16.G3', \
                   fluxtable='cal_spw16.F3inc',reference=fluxcal,transfer=phasecal,
                   incremental=True)


applycal(vis=spw16vis,field=fluxcal, \
         gaintable=['cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.K0',
                    'cal_spw16.B0','cal_spw16.G1int','cal_spw16.G2'], \
         gainfield=['','','','',fluxcal,fluxcal],
         interp=['','','nearest','nearest','nearest','nearest'], \
         parang=False,calwt=False)
#
applycal(vis=spw16vis,field=phasecal, \
         gaintable=['cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.K0',
                    'cal_spw16.B0','cal_spw16.G1int','cal_spw16.G2',
                    'cal_spw16.F3inc'], \
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','nearest','nearest',''], \
         parang=False,calwt=False)
#
applycal(vis=spw16vis,field=source, \
         gaintable=['cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.K0',
                    'cal_spw16.B0','cal_spw16.G1inf','cal_spw16.G2',
                    'cal_spw16.F3inc'], \
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','linear','linear',''], \
         parang=False,calwt=False)

imagename = 'CbandCarray_spw16_raw_continuum_cal_dirty'
clean(vis=spw16vis,
      imagename=imagename,
      field=source,
      weighting='briggs', imsize=[256,256], cell=['1.0 arcsec'],
      mode='mfs', threshold='20 mJy', niter=0,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)


spw17vis='CbandCarray_spw17_raw_continuum.ms'
split(vis=vis, outputvis=spw17vis, datacolumn='data', spw='17')
applycal(vis=spw17vis,field=fluxcal, \
         gaintable=['cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.K0',
                    'cal_spw16.B0','cal_spw16.G1int','cal_spw16.G2'], \
         gainfield=['','','','',fluxcal,fluxcal],
         interp=['','','nearest','nearest','nearest','nearest'], \
         parang=False,calwt=False)
#
applycal(vis=spw17vis,field=phasecal, \
         gaintable=['cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.K0',
                    'cal_spw16.B0','cal_spw16.G1int','cal_spw16.G2',
                    'cal_spw16.F3inc'], \
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','nearest','nearest',''], \
         parang=False,calwt=False)
#
applycal(vis=spw17vis,field=source, \
         gaintable=['cal_spw16.antpos','cal_spw16.gaincurve','cal_spw16.K0',
                    'cal_spw16.B0','cal_spw16.G1inf','cal_spw16.G2',
                    'cal_spw16.F3inc'], \
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','linear','linear',''], \
         parang=False,calwt=False)

spw16vis='CbandCarray_spw16_raw_continuum.ms'
split(vis=spw16vis, outputvis='CbandCarray_spw16_cal_continuum.ms', width=128, datacolumn='corrected', spw='0')
spw17vis='CbandCarray_spw17_raw_continuum.ms'
split(vis=spw17vis, outputvis='CbandCarray_spw17_cal_continuum.ms', width=1024, datacolumn='corrected', spw='0')


imagename = 'CbandCarray_spw17_continuum_cal_dirty'
clean(vis=spw17vis,
      imagename=imagename,
      field=source,
      weighting='briggs', imsize=[256,256], cell=['1.0 arcsec'],
      mode='mfs', threshold='20 mJy', niter=0,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)


imagename = 'CbandCarray_spw17_continuum_cal_clean'
clean(vis=spw17vis,
      imagename=imagename,
      field=source,
      weighting='briggs', imsize=[256,256], cell=['1.0 arcsec'],
      mode='mfs', threshold='20 mJy', niter=10000,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)

