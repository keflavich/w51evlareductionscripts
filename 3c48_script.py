rawvis='13A-064.sb18020284.eb19181492.56353.71736577546.ms'
vis = '3c48_Ku.ms'
flux_calibrator = '0137+331=3C48'
refant='ea04'
split(vis=rawvis, outputvis=vis, field=flux_calibrator, datacolumn='data', spw='')
setjy(vis=vis, field=flux_calibrator, scalebychan=True, modimage='3C48_C.im', usescratch=False)
gencal(vis=vis,caltable='calKu.gaincurve',caltype='gc')
gaincal(vis=vis,caltable='calKu.G0',field=flux_calibrator, spw='',
    gaintable=['calKu.gaincurve'],
    gaintype='G',refant=refant, calmode='p',solint='int',minsnr=3,gaincurve=False)
plotcal(caltable='calKu.G0',xaxis='time',yaxis='phase', figfile='plots/3c48_phasecal_phase.png')
gaincal(vis=vis,caltable='calKu.K0',
    gaintable=['calKu.gaincurve','calKu.G0'],
    field=flux_calibrator,spw='',gaintype='K',gaincurve=False,
    refant=refant,combine='scan',solint='inf',minsnr=3)
plotcal(caltable='calKu.G0',xaxis='time',yaxis='phase', figfile='plots/3c48_ampcal_phase.png')
plotcal(caltable='calKu.G0',xaxis='time',yaxis='amp', figfile='plots/3c48_ampcal_amp.png')
bandpass(vis=vis,caltable='calKu.B0',
    gaintable=['calKu.gaincurve', 'calKu.G0','calKu.K0'],
    field=flux_calibrator,refant=refant,solnorm=False,
    bandtype='B', combine='scan', solint='inf', gaincurve=False)
plotcal(caltable='calKu.B0',xaxis='freq',yaxis='amp', figfile='plots/3c48_bandcal_amp.png')
plotcal(caltable='calKu.B0',xaxis='freq',yaxis='phase', figfile='plots/3c48_bandcal_phase.png')
gaincal(vis=vis,caltable='calKu.G1int',
    gaintable=['calKu.gaincurve',
              'calKu.K0','calKu.B0'],
    field=flux_calibrator,refant=refant,solnorm=F,
    spw='', solint='int',gaintype='G',calmode='p',gaincurve=False,)
plotcal(caltable='calKu.G1int',xaxis='time',yaxis='phase', figfile='plots/3c48_G1cal_phase.png')
plotcal(caltable='calKu.G1int',xaxis='time',yaxis='amp', figfile='plots/3c48_G1cal_amp.png')

gaincal(vis=vis, caltable='calKu.G2', 
        gaintable=['calKu.gaincurve',
                   'calKu.K0','calKu.B0','calKu.G1int'], 
        gainfield=['','',flux_calibrator,flux_calibrator,flux_calibrator], 
        interp=['','','nearest','nearest','nearest'], 
        field=flux_calibrator,refant=refant,solnorm=F,
        spw='',
        solint='inf',combine='scan',gaintype='G',calmode='a',gaincurve=False)
gaincal(vis=vis, caltable='calKu.G3', 
        gaintable=['calKu.gaincurve',
                   'calKu.K0','calKu.B0','calKu.G1int'], 
        gainfield=['','',flux_calibrator,flux_calibrator,flux_calibrator], 
        interp=['','','nearest','nearest','nearest'], 
        field=flux_calibrator,refant=refant,solnorm=F,
        spw='',
        solint='inf',combine='scan',gaintype='G',calmode='a',gaincurve=False)

plotcal(caltable='calKu.G2',xaxis='time',yaxis='phase', figfile='plots/3c48_G2cal_phase.png')
plotcal(caltable='calKu.G2',xaxis='time',yaxis='amp', figfile='plots/3c48_G2cal_amp.png')
plotcal(caltable='calKu.G3',xaxis='time',yaxis='phase', figfile='plots/3c48_G3cal_phase.png')
plotcal(caltable='calKu.G3',xaxis='time',yaxis='amp', figfile='plots/3c48_G3cal_amp.png')

clean(vis=vis, imagename='3c48_Ku_junk', imsize=1024)

applycal(vis=vis, field=flux_calibrator, 
        gaintable=['calKu.gaincurve','calKu.G0','calKu.K0','calKu.B0','calKu.G1int','calKu.G2'],
        interp=['','nearest','nearest','nearest','nearest','nearest'],
        parang=False, calwt=False, gaincurve=False)

clean(vis=vis, imagename='3c48_Ku', imsize=1024)
