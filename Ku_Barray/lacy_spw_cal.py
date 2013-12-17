# Use importevla to import the ASDM as a measurement set, then
# use split to split off spw0 and create barray_spw0.ms


vis = '13A-064.sb24208616.eb26783844.56566.008853900465.ms'
split(vis=vis,datacolumn='data',spw='0',outputvis='barray_spw0.ms')

listobs(vis='barray_spw0.ms')

# unflag all data
flagdata(vis='barray_spw0.ms', mode='unflag')

# flag 1st scan (non-science)
flagdata(vis='barray_spw0.ms', flagbackup=T, 
         mode='manual', scan='1')

#quack start of scans
flagdata(vis='barray_spw0.ms', mode='quack', 
         quackinterval=10.0, quackmode='beg')


# data on phase and target badly affected by RFI early on
flagdata(vis='barray_spw0.ms', mode='manual', 
         timerange='<02:10:00',field='4,5')

# lower edge channels have almost zero signal
flagdata(vis='barray_spw0.ms', mode='manual', 
         spw='0:0~5',field='')




#setjy 
setjy(vis='barray_spw0.ms',field='2',modimage='3C286_U.im',standard='Perley-Butler 2010',scalebychan=T,spw='')

# initial calibration to align phases for BP
gaincal(vis='barray_spw0.ms',caltable='barray_spw0.prebandpass',field='2,4',refant='ea20',gaintype='G',calmode='p',solint='int')
plotcal('barray_spw0.prebandpass',yaxis='phase',iteration='antenna')

#Looks OK, so proceed to do phase cal on BP calibrator
gaincal(vis='barray_spw0.ms',caltable='barray_spw0.prebandpass2',field='2',refant='ea20',gaintype='G',calmode='p',solint='int')

# do a delay cal to be on the safe side...
gaincal(vis='barray_spw0.ms',caltable='barray_spw0.K0', 
        field='2',refant='ea20',spw='0:5~122',gaintype='K', 
        solint='inf',combine='scan',minsnr=5,
        gaintable=['barray_spw0.prebandpass2'])
plotcal(caltable='barray_spw0.K0',xaxis='antenna',yaxis='delay')

#Delay cal looks fine, proceed to BP cal

bandpass(vis='barray_spw0.ms',caltable='barray_spw0.B0',
         field='2',spw='',refant='ea20',solnorm=True,combine='scan', 
         solint='inf',bandtype='B',
         gaintable=['barray_spw0.prebandpass2',
                    'barray_spw0.K0'])

# edge channels 0-4 have poor solns, otherwise OK (I put a flag command in
# near the top)


plotcal(caltable= 'barray_spw0.B0',poln='R', 
        xaxis='chan',yaxis='amp',field='2',subplot=221, 
        iteration='antenna')

plotcal(caltable= 'barray_spw0.B0',poln='L', 
        xaxis='chan',yaxis='amp',field='2',subplot=221, 
        iteration='antenna')

plotcal(caltable= 'barray_spw0.B0',poln='R', 
        xaxis='chan',yaxis='phase',field='2',subplot=221, 
        iteration='antenna')

plotcal(caltable= 'barray_spw0.B0',poln='L', 
        xaxis='chan',yaxis='phase',field='2',subplot=221, 
        iteration='antenna')

# Now do phase/amp cals:
gaincal(vis='barray_spw0.ms',caltable='barray_spw0.G1',
        field='2',spw='0:5~122',
        solint='inf',refant='ea20',gaintype='G',calmode='ap',solnorm=F,
        gaintable=['barray_spw0.K0',
                   'barray_spw0.B0'])


gaincal(vis='barray_spw0.ms',caltable='barray_spw0.G1',
        field='4',spw='0:5~122',
        solint='inf',refant='ea20',gaintype='G',calmode='ap',
        gaintable=['barray_spw0.K0',
                   'barray_spw0.B0'],append=True)

plotcal(caltable='barray_spw0.G1',xaxis='time',yaxis='phase',
        poln='R',plotrange=[-1,-1,-180,180],iteration='antenna',subplot=311)
plotcal(caltable='barray_spw0.G1',xaxis='time',yaxis='phase',
        poln='L',plotrange=[-1,-1,-180,180],iteration='antenna',subplot=311)
plotcal(caltable='barray_spw0.G1',xaxis='time',yaxis='amp',
        poln='R',iteration='antenna',subplot=311)
plotcal(caltable='barray_spw0.G1',xaxis='time',yaxis='amp',
        poln='L',iteration='antenna',subplot=311)

# all cals look good

# Proceed to fluxscale:

myscale = fluxscale(vis='barray_spw0.ms',
                    caltable='barray_spw0.G1', 
                    fluxtable='barray_spw0.fluxscale1', 
                    reference=['2'],
                    transfer=['4'])

# now run the applycals


applycal(vis='barray_spw0.ms',
         field='2',
         gaintable=['barray_spw0.fluxscale1',
                    'barray_spw0.K0',
                    'barray_spw0.B0'],
         gainfield=['2','',''], 
         interp=['nearest','',''],
         calwt=F)

applycal(vis='barray_spw0.ms',
         field='4',
         gaintable=['barray_spw0.fluxscale1',
                    'barray_spw0.K0',
                    'barray_spw0.B0'],
         gainfield=['4','',''], 
         interp=['nearest','',''],
         calwt=F)

applycal(vis='barray_spw0.ms',
         field='5',
         gaintable=['barray_spw0.fluxscale1',
                    'barray_spw0.K0',
                    'barray_spw0.B0'],
         gainfield=['4','',''], 
         interp=['linear','',''],
         calwt=F)

clean(vis='barray_spw0.ms',imagename='test_spw0',field='5',niter=500,mode='mfs',threshold='1mJy',cell='0.1arcsec',interactive=True,imsize=[512,512])
