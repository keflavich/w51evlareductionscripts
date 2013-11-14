import itertools
from collections import defaultdict
import pylab as pl

"""
------------------------------
Arcsinh Colorbar Normalization
------------------------------

For use with, e.g., imshow -
imshow(myimage, norm=AsinhNorm())

Some of the ideas used are from `aplpy <aplpy.github.com>`_


"""
from matplotlib.colors import Normalize
from matplotlib.cm import cbook
from numpy import ma
import numpy as np

class AsinhNorm(Normalize):
    def __init__(self, vmin=None, vmax=None, clip=False, vmid=None):
        self.vmid = vmid
        self.vmin = vmin
        self.vmax = vmax
        self.clip = clip

    def __call__(self,value, clip=None, midpoint=None):


        if clip is None:
            clip = self.clip

        if cbook.iterable(value):
            vtype = 'array'
            val = ma.asarray(value).astype(np.float)
        else:
            vtype = 'scalar'
            val = ma.array([value]).astype(np.float)

        self.autoscale_None(val)
        vmin, vmax = self.vmin, self.vmax

        vmid = self.vmid if self.vmid is not None else (vmax+vmin)/2.0

        if midpoint is None:
            midpoint = (vmid - vmin) / (vmax - vmin)

        if vmin > vmax:
            raise ValueError("minvalue must be less than or equal to maxvalue")
        elif vmin==vmax:
            return 0.0 * val
        else:
            if clip:
                mask = ma.getmask(val)
                val = ma.array(np.clip(val.filled(vmax), vmin, vmax),
                                mask=mask)
            result = (val-vmin) * (1.0/(vmax-vmin))
            #result = (ma.arcsinh(val)-np.arcsinh(vmin))/(np.arcsinh(vmax)-np.arcsinh(vmin))
            result = ma.arcsinh(result/midpoint) / ma.arcsinh(1./midpoint)
        if vtype == 'scalar':
            result = result[0]
        return result

    def autoscale_None(self, A):
        ' autoscale only None-valued vmin or vmax'
        if self.vmin is None:
            self.vmin = ma.min(A)
        if self.vmax is None:
            self.vmax = ma.max(A)
        if self.vmid is None:
            self.vmid = (self.vmax+self.vmin)/2.0



        #return np.arcsinh(array/midpoint) / np.arcsinh(1./midpoint)

def plot_everything(vis, ydatacolumn='data', async=False):

    xaxes = ['frequency','antenna','baseline','uvdist','time',]
    yaxes = ['phase','amp']


    d_avgchannel = defaultdict(lambda:'32')
    d_avgchannel['frequency'] = ''
    d_avgtime = defaultdict(lambda:'60s')
    d_avgtime['time'] = ''

    d_coloraxis = {'time': 'antenna1', 'frequency': 'antenna1', 'antenna':'corr',
                 'baseline':'corr', 'uvdist':'corr'}

    for x,y in itertools.product(xaxes,yaxes):
        plotfile = '{ms}_{dc}_{x}_vs_{y}.png'.format(
                    ms=vis.replace(".ms",""), x=x, y=y,
                    dc=ydatacolumn)
        #print "Attempting to plot %s vs %s with outfile %s" % (x,y,plotfile)
        #print "Plot command: "
        plotms(vis=vis,xaxis=x,yaxis=y,
                avgchannel=d_avgchannel[x],
                avgtime=d_avgtime[x],
                coloraxis=d_coloraxis[x],
                async=async,
                ydatacolumn=ydatacolumn,
                plotfile=plotfile,
                overwrite=True,
                interactive=True,
                expformat='png',
                highres=True,
                )
        plotxy(vis=vis, xaxis=x, yaxis=y, datacolumn=ydatacolumn,
               timebin=d_avgtime[x].strip('s'),
               width=d_avgchannel[x],
               multicolor=d_coloraxis[x],
               async=async,
               figfile=plotfile,
               interactive=True)

        print """plotms(vis='{vis}',xaxis='{xaxis}',yaxis='{yaxis}',
                avgchannel='{avgchannel}',
                avgtime='{avgtime}',
                coloraxis='{coloraxis}',
                async={async},
                ydatacolumn='{ydatacolumn}',
                plotfile='{plotfile}',
                overwrite=True,
                interactive=True,
                )""".format(**dict(vis=vis,xaxis=x,yaxis=y,
                avgchannel=d_avgchannel[x],
                avgtime=d_avgtime[x],
                coloraxis=d_coloraxis[x],
                async=async,
                ydatacolumn=ydatacolumn,
                plotfile=plotfile,
                expformat='png',
                highres=True,
                ))

def plot_amp_vs_time(vis,name,overwrite=True,skipspw=[], figsize=(12,12), field=''):
    ms.open(vis)
    spwinfo = ms.getspectralwindowinfo()

    spws = spwinfo.keys()

    print "Plotting amp vs time for spws: ",spws

    fig = pl.figure(figsize=(12,12))

    for spw in spws:
        if int(spw) in skipspw:
            continue

        print "Selecting %s..." % spw,
        if not ms.selectinit(datadescid=0, reset=True):
            ms.close()
            raise ValueError("MS selection failed.")
        if not ms.msselect({'spw':str(spw),'field':field}):
            print "Failed to select spw %s.  Skipping." % spw
            continue

        print "Loading spw %s..." % spw,
        d = ms.getdata(['amplitude','axis_info','uvdist'],ifraxis=True)
        sortorder = np.argsort(d['uvdist'][:,0])
        amp = d['amplitude'][:,:,sortorder,:]
        chavg_pol1 = amp[0,10:-10,:,:].mean(axis=0)
        chavg_pol2 = amp[1,10:-10,:,:].mean(axis=0)
        timeavg_pol1 = amp[0,:,:,:].mean(axis=2)
        timeavg_pol2 = amp[1,:,:,:].mean(axis=2)
        antavg_pol1 = amp[0,:,:,:].mean(axis=1)
        antavg_pol2 = amp[1,:,:,:].mean(axis=1)

        print "Plotting spw %s..." % spw
        pl.clf()
        pl.title("Channel Average, Polarization 1, SPW %s" % spw)
        pl.imshow(chavg_pol1, aspect=chavg_pol1.shape[1]/float(chavg_pol1.shape[0]), norm=AsinhNorm(), interpolation='nearest')
        pl.ylabel("Baseline")
        pl.xlabel("Time")
        pl.colorbar()
        pl.savefig(name+"_spw%i_chanavg_pol1.png" % (int(spw)), bbox_inches='tight')

        pl.clf()
        pl.title("Channel Average, Polarization 2, SPW %s" % spw)
        pl.imshow(chavg_pol2, aspect=chavg_pol2.shape[1]/float(chavg_pol2.shape[0]), norm=AsinhNorm(), interpolation='nearest')
        pl.ylabel("Baseline")
        pl.xlabel("Time")
        pl.colorbar()
        pl.savefig(name+"_spw%i_chanavg_pol2.png" % (int(spw)), bbox_inches='tight')

        pl.clf()
        pl.title("Time Average, Polarization 1, SPW %s" % spw)
        pl.imshow(timeavg_pol1, aspect=timeavg_pol1.shape[1]/float(timeavg_pol1.shape[0]), norm=AsinhNorm(), interpolation='nearest')
        pl.xlabel("Baseline")
        pl.ylabel("Channel")
        pl.colorbar()
        pl.savefig(name+"_spw%i_timeavg_pol1.png" % (int(spw)), bbox_inches='tight')

        pl.clf()
        pl.title("Time Average, Polarization 2, SPW %s" % spw)
        pl.imshow(timeavg_pol2, aspect=timeavg_pol2.shape[1]/float(timeavg_pol2.shape[0]), norm=AsinhNorm(), interpolation='nearest')
        pl.xlabel("Baseline")
        pl.ylabel("Channel")
        pl.colorbar()
        pl.savefig(name+"_spw%i_timeavg_pol2.png" % (int(spw)), bbox_inches='tight')


        pl.clf()
        pl.title("Baseline Average, Polarization 1, SPW %s" % spw)
        pl.imshow(antavg_pol1, aspect=antavg_pol1.shape[1]/float(antavg_pol1.shape[0]), norm=AsinhNorm(), interpolation='nearest')
        pl.xlabel("Time")
        pl.ylabel("Channel")
        pl.colorbar()
        pl.savefig(name+"_spw%i_antavg_pol1.png" % (int(spw)), bbox_inches='tight')

        pl.clf()
        pl.title("Baseline Average, Polarization 2, SPW %s" % spw)
        pl.imshow(antavg_pol2, aspect=antavg_pol2.shape[1]/float(antavg_pol2.shape[0]), norm=AsinhNorm(), interpolation='nearest')
        pl.xlabel("Time")
        pl.ylabel("Channel")
        pl.colorbar()
        pl.savefig(name+"_spw%i_antavg_pol2.png" % (int(spw)), bbox_inches='tight')

        # explicit cleanup
        pl.clf()
        del d,amp,antavg_pol1,antavg_pol2,timeavg_pol1,timeavg_pol2,chavg_pol1,chavg_pol2
        
    # apparently we have to close each time... great.
    # (or just reset!)
    ms.close()
    pl.close(fig.number)




        #print "Plotting spw ",spw
        #plotms(vis=vis,
        #       spw=str(spw),
        #       xaxis='time',
        #       yaxis='amp',
        #       averagedata=True,
        #       avgchannel='128',
        #       coloraxis='antenna1',
        #       customflaggedsymbol=True,
        #       flaggedsymbolshape = 'diamond',
        #       flaggedsymbolsize =          1,
        #       title='SPW %s channel-avg antenna-color' % spw,
        #       plotfile=name+"_spw%i_chanavg_antcolor.png" % spw,
        #       overwrite=overwrite,
        #       highres=True
        #       )
        #plotms(vis=vis,
        #       spw=str(spw),
        #       xaxis='time',
        #       yaxis='amp',
        #       averagedata=True,
        #       avgbaseline=True,
        #       coloraxis='corr',
        #       customflaggedsymbol=True,
        #       flaggedsymbolshape = 'diamond',
        #       flaggedsymbolsize =          1,
        #       title='SPW %s baseline-avg corr-color' % spw,
        #       plotfile=name+"_spw%i_baseavg_corrcolor.png" % spw,
        #       overwrite=overwrite,
        #       highres=True
        #       )
        #plotms(vis=vis,
        #       spw=str(spw),
        #       xaxis='time',
        #       yaxis='amp',
        #       averagedata=True,
        #       avgantenna=True,
        #       coloraxis='antenna1',
        #       customflaggedsymbol=True,
        #       flaggedsymbolshape = 'diamond',
        #       flaggedsymbolsize =          1,
        #       title='SPW %s antenna-avg antenna-color' % spw,
        #       plotfile=name+"_spw%i_antavg_antcolor.png" % spw,
        #       overwrite=overwrite,
        #       highres=True
        #       )
