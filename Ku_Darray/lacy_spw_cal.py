# Use importevla to import the ASDM as a measurement set, then
# use split to split off spw0 and create darray_spw0.ms

vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

split(vis=vis,datacolumn='data',spw='0',outputvis='darray_spw0.ms')

listobs(vis='darray_spw0.ms')

# unflag all data
flagdata(vis='darray_spw0.ms', mode='unflag')

# flag 1st scan (non-science)
flagdata(vis='darray_spw0.ms', flagbackup=T, 
         mode='manual', scan='1')

#quack start of scans
flagdata(vis='darray_spw0.ms', mode='quack', 
         quackinterval=10.0, quackmode='beg')


# this is for B array...
# data on phase and target badly affected by RFI early on
# flagdata(vis='darray_spw0.ms', mode='manual', 
#          timerange='<02:10:00',field='4,5')

# lower edge channels have almost zero signal
flagdata(vis='darray_spw0.ms', mode='manual', 
         spw='0:0~5',field='')




#setjy 
setjy(vis='darray_spw0.ms',field='0137+331=3C48',model='3C48_U.im',standard='Perley-Butler 2010',scalebychan=T,spw='')

# initial calibration to align phases for BP
gaincal(vis='darray_spw0.ms',caltable='darray_spw0.prebandpass',field='0137+331=3C48,J1922+1530',refant='ea20',gaintype='G',calmode='p',solint='int')
plotcal('darray_spw0.prebandpass',yaxis='phase',iteration='antenna')

#Looks OK, so proceed to do phase cal on BP calibrator
gaincal(vis='darray_spw0.ms',caltable='darray_spw0.prebandpass2',field='0137+331=3C48',refant='ea20',gaintype='G',calmode='p',solint='int')

# do a delay cal to be on the safe side...
gaincal(vis='darray_spw0.ms',caltable='darray_spw0.K0', 
        field='0137+331=3C48',refant='ea20',spw='0:5~122',gaintype='K', 
        solint='inf',combine='scan',minsnr=5,
        gaintable=['darray_spw0.prebandpass2'])
plotcal(caltable='darray_spw0.K0',xaxis='antenna',yaxis='delay')

#Delay cal looks fine, proceed to BP cal

bandpass(vis='darray_spw0.ms',caltable='darray_spw0.B0',
         field='0137+331=3C48',spw='',refant='ea20',solnorm=True,combine='scan', 
         solint='inf',bandtype='B',
         gaintable=['darray_spw0.prebandpass2',
                    'darray_spw0.K0'])

# edge channels 0-4 have poor solns, otherwise OK (I put a flag command in
# near the top)


plotcal(caltable= 'darray_spw0.B0',poln='R', 
        xaxis='chan',yaxis='amp',field='0137+331=3C48',subplot=221, 
        iteration='antenna')

plotcal(caltable= 'darray_spw0.B0',poln='L', 
        xaxis='chan',yaxis='amp',field='0137+331=3C48',subplot=221, 
        iteration='antenna')

plotcal(caltable= 'darray_spw0.B0',poln='R', 
        xaxis='chan',yaxis='phase',field='0137+331=3C48',subplot=221, 
        iteration='antenna')

plotcal(caltable= 'darray_spw0.B0',poln='L', 
        xaxis='chan',yaxis='phase',field='0137+331=3C48',subplot=221, 
        iteration='antenna')

# Now do phase/amp cals:
gaincal(vis='darray_spw0.ms',caltable='darray_spw0.G1',
        field='0137+331=3C48',spw='0:5~122',
        solint='inf',refant='ea20',gaintype='G',calmode='ap',solnorm=F,
        gaintable=['darray_spw0.K0',
                   'darray_spw0.B0'])


gaincal(vis='darray_spw0.ms',caltable='darray_spw0.G1',
        field='J1922+1530',spw='0:5~122',
        solint='inf',refant='ea20',gaintype='G',calmode='ap',
        gaintable=['darray_spw0.K0',
                   'darray_spw0.B0'],append=True)

plotcal(caltable='darray_spw0.G1',xaxis='time',yaxis='phase',
        poln='R',plotrange=[-1,-1,-180,180],iteration='antenna',subplot=311)
plotcal(caltable='darray_spw0.G1',xaxis='time',yaxis='phase',
        poln='L',plotrange=[-1,-1,-180,180],iteration='antenna',subplot=311)
plotcal(caltable='darray_spw0.G1',xaxis='time',yaxis='amp',
        poln='R',iteration='antenna',subplot=311)
plotcal(caltable='darray_spw0.G1',xaxis='time',yaxis='amp',
        poln='L',iteration='antenna',subplot=311)

# all cals look good

# Proceed to fluxscale:

myscale = fluxscale(vis='darray_spw0.ms',
                    caltable='darray_spw0.G1', 
                    fluxtable='darray_spw0.fluxscale1', 
                    reference=['0137+331=3C48'],
                    transfer=['J1922+1530'])

# now run the applycals


applycal(vis='darray_spw0.ms',
         field='0137+331=3C48',
         gaintable=['darray_spw0.fluxscale1',
                    'darray_spw0.K0',
                    'darray_spw0.B0'],
         gainfield=['0137+331=3C48','',''], 
         interp=['nearest','',''],
         calwt=F)

applycal(vis='darray_spw0.ms',
         field='J1922+1530',
         gaintable=['darray_spw0.fluxscale1',
                    'darray_spw0.K0',
                    'darray_spw0.B0'],
         gainfield=['J1922+1530','',''], 
         interp=['nearest','',''],
         calwt=F)

applycal(vis='darray_spw0.ms',
         field='W51 Ku',
         gaintable=['darray_spw0.fluxscale1',
                    'darray_spw0.K0',
                    'darray_spw0.B0'],
         gainfield=['J1922+1530','',''], 
         interp=['linear','',''],
         calwt=F)

clean(vis='darray_spw0.ms',imagename='test_spw0',field='W51 Ku',niter=500,mode='mfs',threshold='1mJy',cell='0.1arcsec',interactive=True,imsize=[512,512])
