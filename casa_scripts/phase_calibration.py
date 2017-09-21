import sys
import os

ms_dataset = sys.argv[-8]
output_path = sys.argv[-7]
flux_cal_field = sys.argv[-6]
phase_cal_field = sys.argv[-5]
spw = sys.argv[-4]
refant = sys.argv[-3]
minsnr = float(sys.argv[-2])
solint = float(sys.argv[-1])

intphase2_gcal = output_path + "/" + 'intphase2.gcal'
tmp_intphase2_gcal = output_path + "/" + 'intphase_tmp2.gcal'  # This is done to keep empty phase gains in intphase.gcal because "append=True" in gaincal throws an error[duplicate phase gains at same time] in subsequent phase calibration run.

amp2_gcal = output_path + "/" + 'amp2.gcal'
tmp_amp2_gcal = output_path + "/" + 'tmp_amp2.gcal'  # same reason as above

bandpass_bcal = output_path + "/" + 'bandpass.bcal'
scanphase_gcal = output_path + "/" + 'scanphase.gcal'
flux_gcal = output_path + "/" + 'flux.gcal'

# copying intphase_gcal to a tmp intphase_gcal and will apply gains using the tmp gcal tables
os.system("cp -r {0} {1}".format(intphase2_gcal, tmp_intphase2_gcal))
os.system("cp -r {0} {1}".format(amp2_gcal, tmp_amp2_gcal))

sys.stdout.write("\n##### Started calculating intphase gains on Phase calibrator#####\n")
gaincal(vis=ms_dataset, caltable=tmp_intphase2_gcal, field=phase_cal_field, spw=spw, refant=refant, calmode='p',
        solint=solint, minsnr=minsnr, gaintable=[bandpass_bcal], append=True)
sys.stdout.write("\n##### Finished calculating intphase gains on Phase calibrator#####\n")

sys.stdout.write("\n##### Started calculating amp gains on Phase calibrator#####\n")
gaincal(vis=ms_dataset, caltable=tmp_amp2_gcal, field=phase_cal_field, spw=spw, refant=refant, calmode='ap',
        solint='inf', minsnr=minsnr, gaintable=[bandpass_bcal, tmp_intphase2_gcal], append=True)
sys.stdout.write("\n##### Finished calculating amp gains on Phase calibrator#####\n")

sys.stdout.write("\n##### Started calculating scanphase gains on Phase calibrator#####\n")
gaincal(vis=ms_dataset, caltable=scanphase_gcal, field=phase_cal_field, spw=spw, refant=refant, calmode='p',
        solint='inf', minsnr=minsnr, gaintable=[bandpass_bcal])
sys.stdout.write("\n##### Finished calculating amp gains on Phase calibrator#####\n")

fluxscale(vis=ms_dataset, caltable=tmp_amp2_gcal, fluxtable=flux_gcal, reference=flux_cal_field)

applycal(vis=ms_dataset, field=phase_cal_field, gaintable=[bandpass_bcal, tmp_intphase2_gcal, flux_gcal],
         gainfield=[flux_cal_field, phase_cal_field, phase_cal_field], calwt=F, applymode='calonly')

os.system("rm -r {0}".format(tmp_intphase2_gcal))
os.system("rm -r {0}".format(tmp_amp2_gcal))