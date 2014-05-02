
# DETAILS:
# SPW 0 looks OK
# SPW 1 had some channels flagged out, but needed more - some time-varying RFI
# SPW 2 doesn't exist
# SPW 3 looks OK; peak amplitudes ~7-8

def diagnostics(vis, spwlist=range(15)):
    for spw in spwlist:
        plotms(vis=vis, xaxis='channel', yaxis='amp', averagedata=True,
               avgtime='1e6s', coloraxis='baseline',
               plotfile=vis.strip("/")+"_spw%i_ampVSchannel.png" % spw,
               showgui=False, interactive=False, overwrite=True, highres=True)

vis = '12B-365.56285.W51.ms'
flagdata(vis=vis, mode='manual', sp='1:31~50') # RFI?
