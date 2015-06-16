"""
Added June 15, 2015:

    These are the flags stated in the pipeline e-mail:
- ea23, due to a deformatter error affecting A0C0, spw='0~8' have been flagged. 

- spw='0,9', where flagged by the pipeline, may be the result of the pipeline confusing a steep baseband shape for RFI/hardware issues. Please check these data and unflag as needed. 

- If your science involves spectral lines, you should be aware of the following:

1) The pipeline applies Hanning-smoothing by default, which may make the calibrated data set not optimal for certain spectral-line science.

2) During the calibration process, several edge channels in each sub band get flagged by default because they are noisier. Therefore, breaks in the frequency span get introduced in the pipeline calibrated data, which in turn may make the output not suitable for certain spectral-line science.

3) The pipeline runs an RFI flagging algorithm which should flag strong lines and may remove spectral lines of interest to your science. 
"""

raise NotImplementedError("Not used.")
vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
flagdata(vis=vis, spw='0~8', antenna='ea23', )
