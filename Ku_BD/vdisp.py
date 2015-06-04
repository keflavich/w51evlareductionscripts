import numpy as np
from astropy import table
from astropy import units as u


tbl22 = table.Table.read(paths.tpath('H2CO22_emission_spectral_fits.ecsv'), format='ascii.ecsv')
tbl77 = table.Table.read(paths.tpath('H77a_spectral_fits.ipac'), format='ascii.ipac')

cluster_sources = ['e8mol', 'e10mol', 'e1', 'e2', 'e3', 'e4', 'e8']
cluster_sources_optimistic = ['e8mol', 'e10mol', 'e1', 'e2', 'e3', 'e4', 'e8', 'e9', 'e10']

velocities = ([row['$V_{LSR}$'] for row in tbl22 if row['Object Name'] in cluster_sources] +
              [row['H77a_velocity'] for row in tbl77 if row['ObjectName'] in cluster_sources])
print("Velocity dispersion including only solid detections: {0}".format(np.std(velocities)))
velocities_optimistic = ([row['$V_{LSR}$'] for row in tbl22 if row['Object Name'] in cluster_sources_optimistic] +
                         [row['H77a_velocity'] for row in tbl77 if row['ObjectName'] in cluster_sources_optimistic])
print("Velocity dispersion including weak detections: {0}".format(np.std(velocities_optimistic)))


# obsolete
#sp = [pyspeckit.Spectrum(x) for x in
#      glob.glob("H77a_BDarray_speccube_uniform_contsub_cvel_big*fits")]
#spectra = sp
#
## conversion....
#[s.xarr.convert_to_unit('km/s') for s in sp]
#
## setup
#for s in sp:
#    s.specname = s.fileprefix.split("_")[-1]
#    s.error[:] = s.stats((100,120))['std']
#
## fitting
#for s in sp:
#    s.plotter(xmin=-10,xmax=120)
#    s.specfit(fittype='gaussian',
#              guesses=[1,55,10],
#              limited=[(True,False),(False,False),(True,False)])
#    s.plotter.ymin -= 0.0003
#    s.specfit.plotresiduals(axis=s.plotter.axis,clear=False,yoffset=-0.0003,label=False)
#    s.plotter.savefig(s.specname+"_h77a_fit.pdf",bbox_inches='tight')
#
#tbl = table.Table()
#names = table.Column(data=[sp.specname for sp in spectra], name='ObjectName')
#tbl.add_column(names)
#for ii,(parname,unit) in enumerate([('amplitude',u.mJy/u.beam),
#                             ('velocity',u.km/u.s),
#                             ('width',u.km/u.s)]):
#    data = [sp.specfit.parinfo[ii].value
#            for sp in spectra]
#    error = [sp.specfit.parinfo[ii].error
#            for sp in spectra]
#    column = table.Column(data=data,
#                          name='H77a_'+parname,
#                          unit=unit)
#    tbl.add_column(column)
#    column = table.Column(data=error,
#                          name='eH77a_'+parname,
#                          unit=unit)
#    tbl.add_column(column)
#
#tbl.write('H77a_spectral_fits.ipac', format='ascii.ipac')
