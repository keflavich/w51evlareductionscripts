import pyspeckit 
import glob

sp = [pyspeckit.Spectrum(x) for x in glob.glob("H77a_BDarray_speccube_uniform_contsub_cvel_big_*e[123456]*fits")]

# conversion....
[s.xarr.convert_to_unit('km/s') for s in sp]

# setup
for s in sp:
    s.specname = s.fileprefix.split("_")[-1]
    s.error[:] = s.stats((100,120))['std']

# fitting
for s in sp:
    s.plotter(xmin=-10,xmax=120)
    s.specfit()
    s.plotter.ymin -= 0.0003
    s.specfit.plotresiduals(axis=s.plotter.axis,clear=False,yoffset=-0.0003,label=False)
    s.plotter.savefig(s.specname+"_h77a_fit.pdf",bbox_inches='tight')
