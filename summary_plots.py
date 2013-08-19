vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

tb.open(vis+"/ANTENNA")
antnames = tb.getcol("NAME")

for ii in xrange(11):
    plotms(vis=vis, xaxis='frequency', yaxis='amp',spw='', avgtime='1e8',
            avgscan=True, avgantenna=True, coloraxis='corr', uvrange='%i~%iklambda' % (ii*100,(ii+1)*100),
            plotfile='allspw_ampvsfreq_corr.png',ydatacolumn='corrected',xdatacolumn='corrected',overwrite=True)
