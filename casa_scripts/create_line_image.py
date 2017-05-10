import sys
import distutils.util

fitspw = sys.argv[-10]
ms_input = sys.argv[-9]
image_name = "{0}/line_spectral_image".format(sys.argv[-8])
model = sys.argv[-7]
threshold = sys.argv[-6]
imsize = int(sys.argv[-5])
interactive = bool(distutils.util.strtobool(sys.argv[-4]))
robust = float(sys.argv[-3])
cell = sys.argv[-2]
niter = int(sys.argv[-1])
field = '0'

uvcontsub(vis=ms_input, field=field, spw='', fitspw=fitspw, solint='int', fitorder=0)
clean(vis="{0}.contsub".format(ms_input), imagename=image_name, imagermode='csclean', imsize=imsize, cell=[cell],
      mode='channel', weighting='briggs', robust=robust, threshold=threshold, interactive=interactive, niter=niter)
