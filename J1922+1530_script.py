flux_calibrator = '0137+331=3C48'
phase_calibrator = 'J1922+1530'
rawvis='13A-064.sb18020284.eb19181492.56353.71736577546.ms'
vis = 'J1922+1530_Ku.ms'
split(vis=rawvis, outputvis=vis, field=phase_calibrator, datacolumn='data', spw='')
gaincal(vis=vis,caltable='calKu.G1int',
        gaintable=['calKu.gaincurve', 'calKu.K0','calKu.B0'],
        field=phase_calibrator,refant='',solnorm=F, spw='', solint='int',
        gaintype='G', calmode='p', gaincurve=False, append=True)

gaincal(vis=vis,caltable='calKu.G1inf',
        gaintable=[ 'calKu.gaincurve', 'calKu.K0', 'calKu.B0'], 
        field=phase_calibrator, refant='', solnorm=F, spw='', solint='inf',
        gaintype='G', calmode='p', gaincurve=False)

plotcal(caltable='calKu.G1inf',xaxis='time',yaxis='phase', figfile='plots/J1922+1530_phasecal_phase.png')


gaincal(vis=vis, caltable='calKu.G2', 
        gaintable=['calKu.gaincurve',
                   'calKu.K0','calKu.B0','calKu.G1int'],
        gainfield=['','',flux_calibrator,flux_calibrator,phase_calibrator], 
        interp=['','','nearest','nearest','nearest'], 
        field=phase_calibrator,refant='',solnorm=F, 
        spw='',
        solint='inf',gaintype='G',calmode='a',gaincurve=False,append=True)

gaincal(vis=vis, caltable='calKu.G3', 
        gaintable=['calKu.gaincurve',
                   'calKu.K0','calKu.B0','calKu.G1int'],
        gainfield=['','',flux_calibrator,flux_calibrator,phase_calibrator], 
        interp=['','','nearest','nearest','nearest'], 
        field=phase_calibrator,refant='',solnorm=F, 
        spw='',
        solint='inf',combine='scan',gaintype='G',calmode='a',gaincurve=False,append=True)


myflux = fluxscale(vis=vis,caltable='calKu.G3', 
                   fluxtable='calKu.F3inc',reference=flux_calibrator,transfer=phase_calibrator,
                   incremental=True)

