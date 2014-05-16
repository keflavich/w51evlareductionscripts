E-mail from Miller Goss explaining the self-cal approach based on a maser
-------------------------------------------------------------------------
Here is a sample of how your run ONE phase self cal and then a differential phase
(after phases are fixed up ) with Amp with a longer solint.

Run CLEAN in casa - briggs=0, large image,

Start up viewer and get the peak and use the stat button to get the rms.

then run gaincal with say SGR_CPHASE.cal as the caltable- create this table. solnorm
is recommended. phase 1 sec or 3 sec (the current integration period ).
calmode=PHASE = p

after you run this run plotcal to look at the phases and make certain they are
continuous.

edit ?

then applycal with the CPHAS.cal as the


then reimage with tget CLEAN. the model will be applied and the phase only self cal
data is imaged.

(when you set the clean boxes with interactive mode be certain to click on all
channels and all polarizations )


now image again and determine the peak and the rms with viewer of this Phase only
sel cal.

If it improves you may run a second self cal or go straight to a differential phase
and AMP self cal.



Run gaincal with caltable =SGRA_CAMPPH.cal and gaintable =( this is the iunput and
is the LAST cal table ) SGR_CPHASE.cal .  ie apply the old cal table before the
solution is run.

NOW with apply cal you apply BOTH tables _CPHASE.cal and the new table
SGR_CAMPPH.cal

ie the input in apply cal is like =['SGR_CPHSE.cal','SGRA_CAMPPH.cal']





solint now should be say 30 to 60 sec and the calmode is AP for ampl and phase.

OW with apply cal you apply BOTH tables _CPHASE.cal and the new table
SGR_CAMPPH.cal

ie the input in apply cal is like =['SGR_CPHSE.cal','SGRA_CAMPPH.cal']





then image and see if this works  and check the peak and the rms.

YOu use the gaintable in gaincal for differential self cal and then in applycal you
can apply ALL relevent tables.


I was NOT clear about the diffenential self cal in applycal you MUST apply all relevent tables.

ie

Run gaincal with caltable =SGRA_CAMPPH.cal and gaintable =( this is the iunput and
is the LAST cal table ) SGR_CPHASE.cal .  ie apply the old cal table before the
solution is run.

NOW with apply cal you apply BOTH tables _CPHASE.cal and the new table
SGR_CAMPPH.cal

ie the input in apply cal is like =['SGR_CPHSE.cal','SGRA_CAMPPH.cal']


SUMMARY

gaincal -> caltable1
applycal(caltable1)
gaincal -> caltable2
applycal(caltable2)
