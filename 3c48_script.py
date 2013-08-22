rawvis='13A-064.sb18020284.eb19181492.56353.71736577546.ms'
vis = '3c48_Ku.ms'
calibrator = '0137+331=3C48'
split(vis=rawvis, outputvis=vis, field=calibrator, datacolumn='data', spw='')
setjy(vis=vis, field=calibrator, scalebychan=True, modimage='3C48_C.im', usescratch=False)
gencal(vis=vis,caltable='calKu.antpos',caltype='antpos',antenna='')
gencal(vis=vis,caltable='calKu.gaincurve',caltype='gc')
gaincal(vis=vis,caltable='calKu.G0',field=calibrator, spw='',
    gaintable=['calKu.antpos','calKu.gaincurve'],
    gaintype='G',refant='', calmode='p',solint='int',minsnr=3,gaincurve=False)
plotcal(caltable='calKu.G0',xaxis='time',yaxis='phase', figfile='plots/3c48_phasecal_phase.png')
gaincal(vis=vis,caltable='calKu.K0',
    gaintable=['calKu.antpos','calKu.gaincurve','calKu.G0'],
    field=calibrator,spw='',gaintype='K',gaincurve=False,
    refant='',combine='scan',solint='inf',minsnr=3)
plotcal(caltable='calKu.G0',xaxis='time',yaxis='phase', figfile='plots/3c48_ampcal_phase.png')
plotcal(caltable='calKu.G0',xaxis='time',yaxis='amp', figfile='plots/3c48_ampcal_amp.png')
bandpass(vis=vis,caltable='calKu.B0',
    gaintable=['calKu.antpos','calKu.gaincurve', 'calKu.G0','calKu.K0'],
    field=calibrator,refant='',solnorm=False,
    bandtype='B', combine='scan', solint='inf', gaincurve=False)
plotcal(caltable='calKu.B0',xaxis='freq',yaxis='amp', figfile='plots/3c48_bandcal_amp.png')
plotcal(caltable='calKu.B0',xaxis='freq',yaxis='phase', figfile='plots/3c48_bandcal_phase.png')
gaincal(vis=vis,caltable='calKu.G1int',
    gaintable=['calKu.antpos','calKu.gaincurve',
              'calKu.K0','calKu.B0'],
    field='2',refant='',solnorm=F,
    spw='', solint='int',gaintype='G',calmode='p',gaincurve=False,)
plotcal(caltable='calKu.G1int',xaxis='time',yaxis='phase', figfile='plots/3c48_finalcal_phase.png')
plotcal(caltable='calKu.G1int',xaxis='time',yaxis='amp', figfile='plots/3c48_finalcal_amp.png')
clean(vis=vis, imagename='3c48_Ku', imsize=1024)
