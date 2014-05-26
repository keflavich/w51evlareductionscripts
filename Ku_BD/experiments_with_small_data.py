"""
5/7/2014: responding to Baobab's suggestions

   The major issue in the KU B+D+single-dish image is because insufficient
   FOV+over clean. It is better to use a 2 times wider field. Otherwise the
   algorithm can be trapped by the sidelobes pattern propagated from the
   sources outside of the field and then diverge.

   On the trouble shooting part, from the .png figure you attach, we know all
   of the spw are sharing the same issue. let's do everything with just one spw
   first. The SB in the bottom right shows the most clearly the point sources.
   So we many focus on that SB first. Then it is just VLA-level trouble
   shooting.
   >> The problems refer to sources still clearly seen in the residuals and
   >> over-structured residuals

   Before making the self-calibration, there is a simple thing to check. First
   we can plotms the uvdis vs. amp, with all time and BW averaged. A compact
   source becomes something with gaps can because of an overestimate of the
   B-array flux, which artificially produce a hump in the uvdis vs. amp data.
   We can first check we can visually see this hump around the shortest
   uv-distance of the B-array data. Probably start with the single-scale clean
   to see if the problem is alleviated. If there is not significant issue, then
   maybe try a bit the self-calibration. 
   Can you also send me this Ku B+D+single-dish visibility data (just one spw).
   I can aso clean a bit a see what could be the problem.

best wishes,
Baobab

"""

vis = 'test_spw14.2ghz_3s.ms'
clean(vis=vis, imagename='test_sp14.2ghz_3s_4096_0.1as_singlescale_uniform', niter=5000, imsize=[4096,4096], cell=['0.1arcsec'], weighting='uniform', usescratch=True)
clean(vis=vis, imagename='test_sp14.2ghz_3s_4096_0.1as_multiscale_uniform', niter=5000, imsize=[4096,4096], cell=['0.1arcsec'], weighting='uniform', usescratch=True,
      multiscale=[0,3,6,12,24])

selfcal(vis=vis, spwn=0, niter=3, imsize=2048, cell='0.1 arcsec', gaintype='T', solint='60s', minsnr=2)
