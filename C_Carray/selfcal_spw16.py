inputvis = 'CbandCarray_spw16_raw_continuum.ms'
outputvis = 'CbandCarray_spw16_selfcal_continuum.ms'
if not os.path.exists(outputvis):
    split(vis=inputvis, outputvis=outputvis, datacolumn='corrected',
          spw='0', field='W51 Ku', width=8)

threshold = '10 mJy'
multiscale = [0,3,6,12]
smallscalebias = 0.8
refant = 'ea15' # ea15 could be OK too
weighting = 'briggs' # from AMSR_Selfcan_Jan2012: use natural and oversample the beam.
niter = 1000 # maybe 100 for natural, 500 for uniform?  needs experiments
imsize = 160
# debug commands to check for ants:
# plotms(vis=outputvis, xaxis='time', yaxis='phase', antenna='ea14', coloraxis='baseline')
"""
notes:
    imsize 256 with deep clean led to a streaky artifact at 167 degrees in the northwest; imsize 160 cuts that out
    niter = 100 iterated to progressively remove more flux.  niter=1000 is current experiment [2015-06-16 17:42:51]
    weighting = 'natural' produced too much extended emission, which seems hard to model
    multiscale including 24 put too much extended emission in, again seeming to cause problems
    smallscalebias increased to 0.8 because again I think the large-scale emission messes up the image

    the more I go through this, the more it looks like subtle tweaks to the clean are more important than selfcal
"""

# first model, I guess
vis = outputvis
flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
flagdata(vis=vis, field='W51 Ku', mode='manual', antenna='ea08') # looks weird in selfcal
flagdata(vis=vis, mode='clip', clipzeros=True)
flagdata(vis=vis, mode='quack', quackinterval=10)
flagdata(vis=vis, mode='manual', autocorr=True)
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged zeros, and NOTHING from applycal.')

# Deeper clean to establish a reference frame for comparison
# (this illustrated that cleaning to 250 mJy with 500 iters did not work - it put flux in the wrong places)
# this MUST be done first to avoid making an overcleaned model
os.system('rm -rf CbandCarray_spw16_nocal_deep.*')
clean(vis = inputvis,
      spw='0', imagename='CbandCarray_spw16_nocal_deep',
      field='W51 Ku',
      weighting=weighting, imsize=[imsize,imsize], cell=['1.0 arcsec'],
      mode='mfs', threshold='1 mJy', niter=10000,
      multiscale=multiscale,
      smallscalebias=smallscalebias,
      selectdata=True)
exportfits('CbandCarray_spw16_nocal_deep.image','CbandCarray_spw16_nocal_deep.image.fits')
exportfits('CbandCarray_spw16_nocal_deep.model','CbandCarray_spw16_nocal_deep.model.fits')
exportfits('CbandCarray_spw16_nocal_deep.residual','CbandCarray_spw16_nocal_deep.residual.fits')

# remove any leftover model (there should be none)
delmod(vis=vis)
# remove the corrected_data column to clear out any traces of previous self-cal operations
clearcal(vis=vis)
os.system('rm -rf CbandCarray_spw16_clean.*')
# First SHALLOW clean to establish a model
clean(vis=vis, spw='0', imagename='CbandCarray_spw16_clean',
      field='W51 Ku',
      weighting=weighting, imsize=[imsize,imsize], cell=['1.0 arcsec'],
      mode='mfs', threshold=threshold, niter=niter,
      negcomponent=0,
      multiscale=multiscale,
      smallscalebias=smallscalebias,
      selectdata=True)
exportfits('CbandCarray_spw16_clean.image','CbandCarray_spw16_clean.image.fits')
exportfits('CbandCarray_spw16_clean.residual','CbandCarray_spw16_clean.residual.fits')
exportfits('CbandCarray_spw16_clean.model','CbandCarray_spw16_clean.model.fits')


# phases are only changing on ~30s timescales
# (can be verified by setting solint = '5s' and looking;
# there is plenty of s/n in 5s intervals but the phase noise can probably be
# reduced by using higher s/n points)
#solint = '60s'

#delmod(vis=vis)
#setjy(vis=vis, model='ch3oh_1024_chan632.image')
for ii,solint in enumerate(('300s','120s','30s')): # 10 is enough.  5 is probably enough.  3 might even be.

    caltable = 'CbandCarray_spw16_selfcal_phase{0:02d}'.format(ii)
    os.system('rm -r {0}'.format(caltable))
    gaincal(vis=vis,
            field='W51 Ku',
            caltable=caltable,
            spw='',
            # gaintype = 'T' could reduce failed fit errors by averaging pols...
            gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
            solint=solint,
            refant=refant,
            calmode='p',
            combine='scan',
            minsnr=3,
            minblperant=4)
    plotms(caltable, yaxis='phase', coloraxis='antenna1',
           plotfile=caltable+"_phase_vs_time_ant1color.png", overwrite=True)
    applycal(vis=vis,
             gaintable=caltable,
             interp='linear',
             flagbackup=True)
    #flagmanager(vis=vis, mode='restore', versionname='cleanflags')

    os.system('rm -rf CbandCarray_spw16_clean_selfcal{0:02d}.*'.format(ii))
    os.system('rm -rf diff_CbandCarray_spw16_clean_selfcal{0:02d}m*.fits'.format(ii))
    os.system('rm -rf CbandCarray_spw16_clean_selfcal{0:02d}m*'.format(ii))

    clean(vis=vis, spw='0', imagename='CbandCarray_spw16_clean_selfcal{0:02d}'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[imsize,imsize], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=niter,
          multiscale=multiscale,
          smallscalebias=smallscalebias,
          negcomponent=0,
          selectdata=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}.image'.format(ii),
               'CbandCarray_spw16_clean_selfcal{0:02d}.image.fits'.format(ii))
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}.residual'.format(ii),
               'CbandCarray_spw16_clean_selfcal{0:02d}.residual.fits'.format(ii))
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}.model'.format(ii),
               'CbandCarray_spw16_clean_selfcal{0:02d}.model.fits'.format(ii))
    if ii > 0:
        immath(['CbandCarray_spw16_clean_selfcal{0:02d}.image'.format(ii),
                'CbandCarray_spw16_clean_selfcal{0:02d}.image'.format(ii-1)],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='CbandCarray_spw16_clean_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        exportfits('CbandCarray_spw16_clean_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1),
                   'diff_CbandCarray_spw16_clean_selfcal{0:02d}m{1:02d}.image.fits'.format(ii,ii-1), overwrite=True)
        stats = imstat(imagename='CbandCarray_spw16_clean_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)
    else:
        immath(['CbandCarray_spw16_clean_selfcal{0:02d}.image'.format(ii),
                'CbandCarray_spw16_clean.image'],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='CbandCarray_spw16_clean_selfcal{0:02d}mORIG.image'.format(ii))
        exportfits('CbandCarray_spw16_clean_selfcal{0:02d}mORIG.image'.format(ii),
                   'diff_CbandCarray_spw16_clean_selfcal{0:02d}mORIG.image.fits'.format(ii), overwrite=True)
        stats = imstat(imagename='CbandCarray_spw16_clean_selfcal{0:02d}mORIG.image'.format(ii))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)

if ii > 1:
    phasecaltable = caltable
    ii += 1

    caltable = 'CbandCarray_spw16_selfcal_ampphase'
    os.system('rm -r {0}'.format(caltable))
    gaincal(vis=vis,
            field='W51 Ku',
            caltable=caltable,
            spw='',
            # gaintype = 'T' could reduce failed fit errors by averaging pols...
            gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
            solint='inf', # increase solint to reduce flagging.  Phase is definitely stable on these scales
            refant=refant,
            calmode='a',
            combine='scan',
            minsnr=3,
            minblperant=4,
            gaintable=[phasecaltable])


    plotcal(caltable, yaxis='phase', xaxis='amp', figfile=caltable+"_phase_vs_amp_plotcal.png")
    # Miller said to apply both
    applycal(vis=vis,
             gaintable=[phasecaltable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used
    os.system('rm -rf CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.*'.format(ii))
    clean(vis=vis, spw='0', imagename='CbandCarray_spw16_clean_selfcal{0:02d}_ampphase'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[imsize,imsize], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=niter,
          negcomponent=0,
          multiscale=multiscale,
          smallscalebias=smallscalebias,
          selectdata=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.image'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.image.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.model'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.model.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.residual'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.residual.fits'.format(ii), overwrite=True)

    os.system('rm -rf CbandCarray_spw16_clean_ampphase_m_selfcal{0:02d}.image'.format(ii))
    immath(['CbandCarray_spw16_clean_selfcal{0:02d}_ampphase.image'.format(ii),
            'CbandCarray_spw16_clean_selfcal{0:02d}.image'.format(ii-1)],
           mode='evalexpr',
           expr='IM1-IM0',
           outfile='CbandCarray_spw16_clean_ampphase_m_selfcal{0:02d}.image'.format(ii))
    exportfits('CbandCarray_spw16_clean_ampphase_m_selfcal{0:02d}.image'.format(ii),
               'diff_CbandCarray_spw16_clean_ampphase_m_selfcal{0:02d}.image.fits'.format(ii), overwrite=True)
    stats = imstat(imagename='CbandCarray_spw16_clean_ampphase_m_selfcal{0:02d}.image'.format(ii))
    print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)

    # try blcal
    blcaltable = 'CbandCarray_spw16_selfcal_blcal'
    os.system('rm -r {0}'.format(blcaltable))
    blcal(vis=vis, caltable=blcaltable, field='W51 Ku', spw='', solint='inf',
          calmode='ap', gaintable=[caltable, phasecaltable],
          interp='linear')

    # OK to do this here: blcal already computed the next round of calibration but hasn't been applied yet
    os.system('rm -rf CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase.*'.format(ii))
    clean(vis=vis, spw='0', imagename='CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[imsize,imsize], cell=['1.0 arcsec'],
          mode='mfs', threshold='1 mJy', niter=10000,
          negcomponent=0,
          multiscale=multiscale,
          smallscalebias=smallscalebias,
          selectdata=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase.image'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase.image.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase.model'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase.model.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase.residual'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_deep_ampphase.residual.fits'.format(ii), overwrite=True)

    applycal(vis=vis,
             gaintable=[phasecaltable,caltable,blcaltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    os.system('rm -rf CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase.*'.format(ii))
    clean(vis=vis, spw='0', imagename='CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[imsize,imsize], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=niter,
          multiscale=multiscale,
          smallscalebias=smallscalebias,
          selectdata=True)
    exportfits('CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase.image'.format(ii),'CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase.image.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase.model'.format(ii),'CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase.model.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase.residual'.format(ii),'CbandCarray_spw16_clean_selfcal_blcal{0:02d}_ampphase.residual.fits'.format(ii), overwrite=True)


    os.system('rm -rf CbandCarray_spw16_clean_selfcal{0:02d}_deep.*'.format(ii))
    clean(vis=vis, spw='0', imagename='CbandCarray_spw16_clean_selfcal{0:02d}_deep'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[imsize,imsize], cell=['1.0 arcsec'],
          mode='mfs', threshold='1 mJy', niter=10000,
          multiscale=multiscale,
          smallscalebias=smallscalebias,
          selectdata=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_deep.image'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_deep.image.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_deep.model'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_deep.model.fits'.format(ii), overwrite=True)
    exportfits('CbandCarray_spw16_clean_selfcal{0:02d}_deep.residual'.format(ii),'CbandCarray_spw16_clean_selfcal{0:02d}_deep.residual.fits'.format(ii), overwrite=True)

    # look for interesting residuals?
    plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='corrected-model',
           field='W51 Ku', avgtime='30s', plotfile='final_selfcal_amp_vs_uvdist_corrected-model.png', highres=True, overwrite=True)

    plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='corrected',
           field='W51 Ku', avgtime='30s', plotfile='final_selfcal_amp_vs_uvdist_corrected.png', highres=True, overwrite=True)
    plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='model',
           field='W51 Ku', avgtime='30s', plotfile='final_selfcal_amp_vs_uvdist_model_on_corrected.png',
           clearplots=False, highres=True, overwrite=True)
